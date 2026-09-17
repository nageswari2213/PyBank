import streamlit as st
import builtins
from io import StringIO
from contextlib import redirect_stdout

from banking.account import open_account, login
from banking.deposit import deposit_money
from banking.withdraw import withdraw_money
from banking.balance import check_balance
from banking.history import transaction_history, account_summary


def run_function_with_inputs(function, inputs):
    """Run existing terminal-based function using Streamlit inputs."""
    input_values = iter(inputs)
    output = StringIO()

    original_input = builtins.input

    def fake_input(prompt=""):
        return next(input_values)

    builtins.input = fake_input

    try:
        with redirect_stdout(output):
            result = function()
    finally:
        builtins.input = original_input

    return result, output.getvalue()


st.title("WELCOME TO PYBANK")

if "account_number" not in st.session_state:
    st.session_state.account_number = None


if st.session_state.account_number is None:

    option = st.selectbox(
        "Select Option",
        ["Login", "Open New Account"]
    )

    if option == "Open New Account":

        st.header("OPEN NEW ACCOUNT")

        name = st.text_input("Enter your name")
        pin = st.text_input("Enter 4-digit PIN", type="password")

        account_type = st.selectbox(
            "Select Account Type",
            ["SAVINGS", "CURRENT"]
        )

        opening_deposit = st.text_input("Enter opening deposit")

        if st.button("Open Account"):

            if not name or not pin or not opening_deposit:
                st.error("Please fill all fields.")

            else:
                result, output = run_function_with_inputs(
                    open_account,
                    [
                        name,
                        pin,
                        account_type,
                        opening_deposit
                    ]
                )

                st.text(output)

    else:

        st.header("LOGIN")

        account_number = st.text_input("Enter Account Number")
        pin = st.text_input("Enter PIN", type="password")

        if st.button("Login"):

            if not account_number or not pin:
                st.error("Please enter account number and PIN.")

            else:
                result, output = run_function_with_inputs(
                    login,
                    [
                        account_number,
                        pin
                    ]
                )

                st.text(output)

                if result:
                    st.session_state.account_number = result
                    st.rerun()


else:

    account_number = st.session_state.account_number

    st.write("Account Number:", account_number)

    option = st.selectbox(
        "ACCOUNT MENU",
        [
            "Deposit Money",
            "Withdraw Money",
            "Check Balance",
            "Transaction History",
            "Account Summary",
            "Logout"
        ]
    )

    if option == "Deposit Money":

        st.header("DEPOSIT MONEY")

        amount = st.text_input("Enter deposit amount")

        if st.button("Deposit"):

            if not amount:
                st.error("Please enter deposit amount.")

            else:
                result, output = run_function_with_inputs(
                    lambda: deposit_money(account_number),
                    [amount]
                )

                st.text(output)

    elif option == "Withdraw Money":

        st.header("WITHDRAW MONEY")

        amount = st.text_input("Enter withdrawal amount")

        if st.button("Withdraw"):

            if not amount:
                st.error("Please enter withdrawal amount.")

            else:
                result, output = run_function_with_inputs(
                    lambda: withdraw_money(account_number),
                    [amount]
                )

                st.text(output)

    elif option == "Check Balance":

        st.header("BALANCE ENQUIRY")

        if st.button("Check Balance"):

            result, output = run_function_with_inputs(
                lambda: check_balance(account_number),
                []
            )

            st.text(output)

    elif option == "Transaction History":

        st.header("TRANSACTION HISTORY")

        if st.button("Show History"):

            result, output = run_function_with_inputs(
                lambda: transaction_history(account_number),
                []
            )

            st.text(output)

    elif option == "Account Summary":

        st.header("ACCOUNT SUMMARY")

        if st.button("Show Summary"):

            result, output = run_function_with_inputs(
                lambda: account_summary(account_number),
                []
            )

            st.text(output)

    elif option == "Logout":

        st.session_state.account_number = None
        st.rerun()