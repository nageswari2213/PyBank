from banking.account import login


account = login()


if account:
    print("Logged in account:", account)
else:
    print("Login failed.")