import hashlib
from banking.config import get_connection


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


conn = get_connection()

if conn is None:
    print("Database connection failed.")
    exit()

cursor = conn.cursor()

try:
    cursor.execute(
        "SELECT account_number, pin FROM accounts1"
    )

    accounts = cursor.fetchall()

    for account_number, pin in accounts:

        if len(pin) == 64:
            continue

        hashed_pin = hash_pin(pin)

        cursor.execute(
            """
            UPDATE accounts1
            SET pin = %s
            WHERE account_number = %s
            """,
            (hashed_pin, account_number)
        )

        print(f"{account_number}: PIN converted successfully")

    conn.commit()

    print("\nAll old PINs have been converted to SHA-256.")

except Exception as e:
    conn.rollback()
    print("Error:", e)

finally:
    cursor.close()
    conn.close()