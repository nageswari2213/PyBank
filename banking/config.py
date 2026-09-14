import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Nag@221300",
    "database": "banking_db"
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)

    except Error as e:
        print("Database connection error:", e)
        return None


MIN_DEPOSIT = 500
MAX_DEPOSIT = 100000

MIN_WITHDRAWAL = 100
MIN_BALANCE = 1000

DAILY_WITHDRAWAL_LIMIT = 50000

PIN_LENGTH = 4
MAX_FAILED_ATTEMPTS = 3

MIN_OPENING_DEPOSIT = 1000