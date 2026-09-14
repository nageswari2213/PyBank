class PyBankError(Exception):
    pass


class InvalidAmountError(PyBankError):
    pass


class InsufficientBalanceError(PyBankError):
    pass


class MinimumBalanceError(PyBankError):
    pass


class DailyLimitExceededError(PyBankError):
    pass


class InvalidPinError(PyBankError):
    pass


class AccountLockedError(PyBankError):
    pass


class AccountNotFoundError(PyBankError):
    pass