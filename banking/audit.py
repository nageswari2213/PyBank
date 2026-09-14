from banking.config import get_connection


def log_action(account_number, action, details=""):
    """Store an important account action in audit_log."""

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO audit_log
            (
                account_number,
                action,
                details
            )
            VALUES (%s, %s, %s)
            """,
            (
                account_number,
                action,
                details
            )
        )

        conn.commit()

        return True

    except Exception as e:
        conn.rollback()
        print("Audit log error:", e)
        return False

    finally:
        cursor.close()
        conn.close()