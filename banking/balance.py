from banking.config import get_connection
from banking.exceptions import AccountNotFoundError


def check_balance(account_number):
    """Display account balance and account details."""

    print("\n========== BALANCE ENQUIRY ==========")

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor(dictionary=True)

    try:

        # ==========================================
        # 1. FIND ACCOUNT
        # ==========================================

        cursor.execute(
            """
            SELECT
                account_number,
                balance,
                account_type,
                status
            FROM accounts1
            WHERE account_number = %s
            """,
            (account_number,)
        )

        account = cursor.fetchone()

        # ==========================================
        # 2. CHECK ACCOUNT
        # ==========================================

        if account is None:
            raise AccountNotFoundError(
                "Account not found."
            )

        # ==========================================
        # 3. CHECK ACCOUNT STATUS
        # ==========================================

        if account["status"] != "ACTIVE":

            print(
                f"Cannot check balance. "
                f"Account status is {account['status']}."
            )

            return False

        # ==========================================
        # 4. DISPLAY BALANCE
        # ==========================================

        balance = float(account["balance"])

        print("\n===================================")
        print("         ACCOUNT BALANCE")
        print("===================================")
        print("Account Number :", account["account_number"])
        print("Account Type   :", account["account_type"])
        print("Account Status :", account["status"])
        print(f"Available Balance: ₹{balance:.2f}")
        print("===================================")

        # ==========================================
        # 5. RECORD BALANCE CHECK
        # ==========================================

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
                "BALANCE_CHECK",
                0
            )
        )

        conn.commit()

        return True

    except AccountNotFoundError as e:

        print(e)
        return False

    except Exception as e:

        conn.rollback()
        print("Balance enquiry failed:", e)
        return False

    finally:

        cursor.close()
        conn.close()
