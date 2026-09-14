from banking.config import (
    MIN_DEPOSIT,
    MAX_DEPOSIT,
    MIN_WITHDRAWAL,
    MIN_OPENING_DEPOSIT,
    PIN_LENGTH
)

from banking.exceptions import InvalidAmountError


def validate_pin(pin):
    if not pin.isdigit() or len(pin) != PIN_LENGTH:
        raise ValueError("PIN must contain exactly 4 digits.")

    return True


def validate_opening_deposit(amount):
    if amount < MIN_OPENING_DEPOSIT:
        raise InvalidAmountError(
            f"Opening deposit must be at least ₹{MIN_OPENING_DEPOSIT}."
        )

    return True


def validate_deposit(amount):
    if amount < MIN_DEPOSIT:
        raise InvalidAmountError(
            f"Minimum deposit is ₹{MIN_DEPOSIT}."
        )

    if amount > MAX_DEPOSIT:
        raise InvalidAmountError(
            f"Maximum deposit is ₹{MAX_DEPOSIT}."
        )

    return True


def validate_withdrawal(amount):
    if amount < MIN_WITHDRAWAL:
        raise InvalidAmountError(
            f"Minimum withdrawal is ₹{MIN_WITHDRAWAL}."
        )

    return True