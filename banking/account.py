import hashlib
import random

from banking.config import (
    get_connection,
    MAX_FAILED_ATTEMPTS
)

from banking.validators import (
    validate_pin,
    validate_opening_deposit
)

from banking.exceptions import (
    AccountNotFoundError,
    AccountLockedError
)

from banking.audit import log_action


def hash_pin(pin):
    """Convert PIN into SHA-256 hash."""

    return hashlib.sha256(
        pin.encode()
    ).hexdigest()


def generate_account_number():
    """Generate a unique account number."""

    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    try:
        while True:

            number = random.randint(
                100000,
                999999
            )

            account_number = f"ACC{number}"

            cursor.execute(
                """
                SELECT account_number
                FROM accounts1
                WHERE account_number = %s
                """,
                (account_number,)
            )

            if cursor.fetchone() is None:
                return account_number

    finally:
        cursor.close()
        conn.close()


def open_account():
    """Create a new bank account."""

    print("\n========== OPEN NEW ACCOUNT ==========")

    name = input(
        "Enter customer name: "
    ).strip()

    pin = input(
        "Create 4-digit PIN: "
    ).strip()

    try:

        validate_pin(pin)

        account_type = input(
            "Enter account type (SAVINGS/CURRENT): "
        ).strip().upper()

        if account_type not in (
            "SAVINGS",
            "CURRENT"
        ):
            print("Invalid account type.")
            return

        amount = float(
            input("Enter opening deposit: ")
        )

        validate_opening_deposit(amount)

    except ValueError as e:

        print("Invalid input:", e)
        return

    except Exception as e:

        print("Error:", e)
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        # Create customer
        cursor.execute(
            """
            INSERT INTO customers1
            (
                customer_name
            )
            VALUES (%s)
            """,
            (name,)
        )

        customer_id = cursor.lastrowid

        # Generate account number
        account_number = generate_account_number()

        if account_number is None:
            raise Exception(
                "Could not generate account number."
            )

        # Hash PIN
        pin_hash = hash_pin(pin)

        # Create account
        cursor.execute(
            """
            INSERT INTO accounts1
            (
                customer_id,
                account_number,
                balance,
                pin,
                account_type
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                customer_id,
                account_number,
                amount,
                pin_hash,
                account_type
            )
        )

        # Opening deposit transaction
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

        conn.commit()

        # Audit
        log_action(
            account_number,
            "ACCOUNT_CREATED",
            f"New {account_type} account created"
        )

        print("\n========================================")
        print("Account created successfully!")
        print("========================================")
        print("Customer Name :", name)
        print("Account Number:", account_number)
        print("Account Type  :", account_type)
        print(
            f"Opening Balance: ₹{amount:.2f}"
        )
        print("========================================")

    except Exception as e:

        conn.rollback()

        print(
            "Account creation failed:",
            e
        )

    finally:

        cursor.close()
        conn.close()


def login():
    """Login using account number and PIN."""

    print("\n========== PYBANK LOGIN ==========")

    account_number = input(
        "Enter account number: "
    ).strip()

    pin = input(
        "Enter PIN: "
    ).strip()

    try:

        validate_pin(pin)

    except ValueError as e:

        print(e)
        return None

    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                account_number,
                pin,
                failed_attempts,
                status
            FROM accounts1
            WHERE account_number = %s
            """,
            (account_number,)
        )

        account = cursor.fetchone()

        # Account doesn't exist
        if account is None:

            print("Account not found.")

            return None

        # Locked
        if account["status"] == "LOCKED":

            print("Account is locked.")

            log_action(
                account_number,
                "LOGIN_FAILED",
                "Login attempted on locked account"
            )

            return None

        # Inactive
        if account["status"] == "INACTIVE":

            print("Account is inactive.")

            log_action(
                account_number,
                "LOGIN_FAILED",
                "Login attempted on inactive account"
            )

            return None

        # Hash entered PIN
        pin_hash = hash_pin(pin)

        # Correct PIN
        if pin_hash == account["pin"]:

            cursor.execute(
                """
                UPDATE accounts1
                SET failed_attempts = 0
                WHERE account_number = %s
                """,
                (account_number,)
            )

            conn.commit()

            log_action(
                account_number,
                "LOGIN_SUCCESS",
                "Successful login"
            )

            print("\nLogin successful!")

            return account_number

        # Wrong PIN
        failed_attempts = (
            account["failed_attempts"] + 1
        )

        # Lock after 3 attempts
        if failed_attempts >= MAX_FAILED_ATTEMPTS:

            cursor.execute(
                """
                UPDATE accounts1
                SET
                    failed_attempts = %s,
                    status = 'LOCKED'
                WHERE account_number = %s
                """,
                (
                    failed_attempts,
                    account_number
                )
            )

            conn.commit()

            log_action(
                account_number,
                "ACCOUNT_LOCKED",
                "Account locked after 3 wrong PIN attempts"
            )

            print(
                "\nAccount locked after "
                "3 wrong PIN attempts."
            )

        else:

            cursor.execute(
                """
                UPDATE accounts1
                SET failed_attempts = %s
                WHERE account_number = %s
                """,
                (
                    failed_attempts,
                    account_number
                )
            )

            conn.commit()

            remaining = (
                MAX_FAILED_ATTEMPTS
                - failed_attempts
            )

            log_action(
                account_number,
                "LOGIN_FAILED",
                f"Incorrect PIN. Attempts remaining: {remaining}"
            )

            print(
                f"\nIncorrect PIN. "
                f"Attempts remaining: {remaining}"
            )

        return None

    except Exception as e:

        conn.rollback()

        print(
            "Login error:",
            e
        )

        return None

    finally:

        cursor.close()
        conn.close()