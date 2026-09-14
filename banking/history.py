from banking.config import get_connection

from banking.exceptions import AccountNotFoundError


def transaction_history(
    account_number,
    limit=10
):

    print(
        "\n========== TRANSACTION HISTORY =========="
    )

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT account_number
            FROM accounts1
            WHERE account_number = %s
            """,
            (account_number,)
        )

        account = cursor.fetchone()

        if account is None:

            raise AccountNotFoundError(
                "Account not found."
            )

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                transaction_date
            FROM transactions
            WHERE account_number = %s
            ORDER BY transaction_date DESC
            LIMIT %s
            """,
            (
                account_number,
                limit
            )
        )

        transactions = cursor.fetchall()

        if not transactions:

            print("No transactions found.")

            return True

        print(
            "\n-------------------------------------------------------------"
        )

        print(
            f"{'ID':<6}"
            f"{'TYPE':<18}"
            f"{'AMOUNT':<15}"
            f"{'DATE':<22}"
        )

        print(
            "-------------------------------------------------------------"
        )

        for transaction in transactions:

            print(
                f"{transaction['transaction_id']:<6}"
                f"{transaction['transaction_type']:<18}"
                f"₹{float(transaction['amount']):<14.2f}"
                f"{transaction['transaction_date']}"
            )

        print(
            "-------------------------------------------------------------"
        )

        return True

    except AccountNotFoundError as e:

        print(e)

        return False

    except Exception as e:

        print(
            "Transaction history failed:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()


def account_summary(account_number):

    print(
        "\n========== ACCOUNT SUMMARY =========="
    )

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor(
        dictionary=True
    )

    try:

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

        if account is None:

            raise AccountNotFoundError(
                "Account not found."
            )

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(amount), 0)
                AS total_deposits,
                COUNT(*) AS deposit_count
            FROM transactions
            WHERE account_number = %s
              AND transaction_type = 'DEPOSIT'
            """,
            (account_number,)
        )

        deposit_data = cursor.fetchone()

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(amount), 0)
                AS total_withdrawals,
                COUNT(*) AS withdrawal_count
            FROM transactions
            WHERE account_number = %s
              AND transaction_type = 'WITHDRAW'
            """,
            (account_number,)
        )

        withdrawal_data = cursor.fetchone()

        print("\n===================================")
        print("          ACCOUNT SUMMARY")
        print("===================================")
        print(
            "Account Number :",
            account["account_number"]
        )
        print(
            "Account Type   :",
            account["account_type"]
        )
        print(
            "Account Status :",
            account["status"]
        )
        print(
            f"Current Balance: "
            f"₹{float(account['balance']):.2f}"
        )

        print("-----------------------------------")

        print(
            f"Total Deposits : "
            f"₹{float(deposit_data['total_deposits']):.2f}"
        )

        print(
            "Deposit Count  :",
            deposit_data["deposit_count"]
        )

        print(
            f"Total Withdrawals: "
            f"₹{float(withdrawal_data['total_withdrawals']):.2f}"
        )

        print(
            "Withdrawal Count:",
            withdrawal_data["withdrawal_count"]
        )

        print("===================================")

        return True

    except AccountNotFoundError as e:

        print(e)

        return False

    except Exception as e:

        print(
            "Account summary failed:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()