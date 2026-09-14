from banking.account import (
    open_account,
    login
)

from banking.deposit import deposit_money

from banking.withdraw import withdraw_money

from banking.balance import check_balance

from banking.history import (
    transaction_history,
    account_summary
)

from banking.display import (
    show_main_menu,
    show_account_menu
)


def logged_in_menu(account_number):
    """Handle menu after successful login."""

    while True:

        show_account_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            deposit_money(
                account_number
            )

        elif choice == "2":

            withdraw_money(
                account_number
            )

        elif choice == "3":

            check_balance(
                account_number
            )

        elif choice == "4":

            transaction_history(
                account_number
            )

        elif choice == "5":

            account_summary(
                account_number
            )

        elif choice == "6":

            print(
                "\nLogged out successfully."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please enter 1-6."
            )


def main():
    """Start PyBank."""

    print("\n===================================")
    print("       WELCOME TO PYBANK")
    print("===================================")

    while True:

        show_main_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            open_account()

        elif choice == "2":

            account_number = login()

            if account_number:

                logged_in_menu(
                    account_number
                )

        elif choice == "3":

            print(
                "\nThank you for using PyBank!"
            )

            print("Goodbye!")

            break

        else:

            print(
                "\nInvalid choice. "
                "Please enter 1-3."
            )


if __name__ == "__main__":
    main()