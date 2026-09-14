from datetime import date

from banking.config import (
    get_connection,
    MIN_WITHDRAWAL,
    MIN_BALANCE,
    DAILY_WITHDRAWAL_LIMIT
)

from banking.validators import validate_withdrawal

from banking.exceptions import (
    AccountNotFoundError,
    InsufficientBalanceError,
    MinimumBalanceError,
    DailyLimitExceededError,
    InvalidAmountError
)

from banking.audit import log_action


def withdraw_money(account_number):
    """Withdraw money from an existing bank account."""

    print("\n========== WITHDRAW MONEY ==========")

    try:
        amount = float(input("Enter withdrawal amount: "))

        # Validate withdrawal amount
        validate_withdrawal(amount)

    except (ValueError, InvalidAmountError) as e:
        print("Invalid input:", e)
        return False

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor(dictionary=True)

    try:
        # Lock account row while updating
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
                f"Cannot withdraw. "
                f"Account status is {account['status']}."
            )
            conn.rollback()
            return False

        current_balance = float(account["balance"])

        # Check sufficient balance
        if amount > current_balance:
            raise InsufficientBalanceError(
                "Insufficient balance."
            )

        remaining_balance = current_balance - amount

        # Check minimum balance
        if remaining_balance < MIN_BALANCE:
            raise MinimumBalanceError(
                f"Minimum balance of ₹{MIN_BALANCE} "
                f"must be maintained."
            )

        today = date.today()

        # Check today's withdrawal total
        cursor.execute(
            """
            SELECT total_withdrawn
            FROM daily_withdrawal_limits
            WHERE account_number = %s
              AND withdrawal_date = %s
            FOR UPDATE
            """,
            (account_number, today)
        )

        daily_record = cursor.fetchone()

        if daily_record is None:
            total_withdrawn = 0.0
        else:
            total_withdrawn = float(
                daily_record["total_withdrawn"]
            )

        new_daily_total = total_withdrawn + amount

        # Check daily withdrawal limit
        if new_daily_total > DAILY_WITHDRAWAL_LIMIT:
            raise DailyLimitExceededError(
                f"Daily withdrawal limit of "
                f"₹{DAILY_WITHDRAWAL_LIMIT} exceeded."
            )

        # Update balance
        cursor.execute(
            """
            UPDATE accounts1
            SET balance = %s
            WHERE account_number = %s
            """,
            (remaining_balance, account_number)
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
                "WITHDRAW",
                amount
            )
        )

        # Update daily withdrawal limit
        if daily_record is None:

            cursor.execute(
                """
                INSERT INTO daily_withdrawal_limits
                (
                    account_number,
                    withdrawal_date,
                    total_withdrawn
                )
                VALUES (%s, %s, %s)
                """,
                (
                    account_number,
                    today,
                    amount
                )
            )

        else:

            cursor.execute(
                """
                UPDATE daily_withdrawal_limits
                SET total_withdrawn = %s
                WHERE account_number = %s
                  AND withdrawal_date = %s
                """,
                (
                    new_daily_total,
                    account_number,
                    today
                )
            )

        # Commit all changes
        conn.commit()

        # Audit log
        log_action(
            account_number,
            "WITHDRAW",
            f"Withdrawn ₹{amount:.2f}"
        )

        # Receipt
        print("\n===================================")
        print("       WITHDRAWAL SUCCESSFUL")
        print("===================================")
        print("Account Number  :", account_number)
        print(f"Withdrawn       : ₹{amount:.2f}")
        print(f"Previous Balance: ₹{current_balance:.2f}")
        print(f"New Balance     : ₹{remaining_balance:.2f}")
        print("===================================")

        return True

    except (
        AccountNotFoundError,
        InsufficientBalanceError,
        MinimumBalanceError,
        DailyLimitExceededError
    ) as e:

        conn.rollback()
        print(e)
        return False

    except Exception as e:

        conn.rollback()
        print("Withdrawal failed:", e)
        return False

    finally:
        cursor.close()
        conn.close()