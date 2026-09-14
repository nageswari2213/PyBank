from banking.config import get_connection
from banking.validators import validate_deposit
from banking.exceptions import (
    AccountNotFoundError,
    InvalidAmountError
)
from banking.audit import log_action


def deposit_money(account_number):
    """Deposit money into an existing bank account."""

    print("\n========== DEPOSIT MONEY ==========")

    try:
        amount = float(input("Enter deposit amount: "))

        # Validate deposit amount
        validate_deposit(amount)

    except (ValueError, InvalidAmountError) as e:
        print("Invalid input:", e)
        return False

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor(dictionary=True)

    try:
        # Lock the account row while updating
        cursor.execute(
            """
            SELECT
                account_number,
                balance,
                status
            FROM accounts1
            WHERE account_number = %s
            FOR UPDATE
            """,
            (account_number,)
        )

        account = cursor.fetchone()

        # Account does not exist
        if account is None:
            raise AccountNotFoundError("Account not found.")

        # Account must be active
        if account["status"] != "ACTIVE":
            print(
                f"Cannot deposit. "
                f"Account status is {account['status']}."
            )
            conn.rollback()
            return False

        old_balance = float(account["balance"])
        new_balance = old_balance + amount

        # Update account balance
        cursor.execute(
            """
            UPDATE accounts1
            SET balance = %s
            WHERE account_number = %s
            """,
            (new_balance, account_number)
        )

        # Record transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (
                account_number,
                transaction_type,
                amount
            )
            VALUES (%s, %s, %s)
            """,
            (
                account_number,
                "DEPOSIT",
                amount
            )
        )

        # Commit database changes
        conn.commit()

        # Add audit log
        log_action(
            account_number,
            "DEPOSIT",
            f"Deposited ₹{amount:.2f}"
        )

        # Receipt
        print("\n===================================")
        print("        DEPOSIT SUCCESSFUL")
        print("===================================")
        print("Account Number :", account_number)
        print(f"Deposited      : ₹{amount:.2f}")
        print(f"Previous Balance: ₹{old_balance:.2f}")
        print(f"New Balance     : ₹{new_balance:.2f}")
        print("===================================")

        return True

    except AccountNotFoundError as e:
        conn.rollback()
        print(e)
        return False

    except Exception as e:
        conn.rollback()
        print("Deposit failed:", e)
        return False

    finally:
        cursor.close()
        conn.close()