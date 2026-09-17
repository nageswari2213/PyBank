import tkinter as tk
from tkinter import messagebox
import builtins
import io
from contextlib import redirect_stdout

from banking.account import open_account, login
from banking.deposit import deposit_money
from banking.withdraw import withdraw_money
from banking.balance import check_balance
from banking.history import transaction_history, account_summary


# ============================================================
# HELPER FUNCTION
# ============================================================

def run_function_with_input(function, inputs, *args):
    """
    Run existing banking functions by providing GUI input
    instead of terminal input.
    """
    input_values = iter(inputs)
    output = io.StringIO()

    original_input = builtins.input

    def gui_input(prompt=""):
        return next(input_values)

    builtins.input = gui_input

    try:
        with redirect_stdout(output):
            result = function(*args)
        return result, output.getvalue()

    except Exception as e:
        return False, str(e)

    finally:
        builtins.input = original_input


# ============================================================
# OPEN ACCOUNT
# ============================================================

def open_account_window():

    window = tk.Toplevel(root)
    window.title("Open New Account")
    window.geometry("450x500")
    window.resizable(False, False)

    tk.Label(
        window,
        text="OPEN NEW ACCOUNT",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Customer Name").pack()
    name_entry = tk.Entry(window, width=35)
    name_entry.pack(pady=5)

    tk.Label(window, text="4-Digit PIN").pack()
    pin_entry = tk.Entry(window, width=35, show="*")
    pin_entry.pack(pady=5)

    tk.Label(window, text="Account Type").pack()

    account_type = tk.StringVar()
    account_type.set("SAVINGS")

    account_type_menu = tk.OptionMenu(
        window,
        account_type,
        "SAVINGS",
        "CURRENT"
    )
    account_type_menu.pack(pady=5)

    tk.Label(window, text="Opening Deposit").pack()
    deposit_entry = tk.Entry(window, width=35)
    deposit_entry.pack(pady=5)

    def create_account():

        name = name_entry.get().strip()
        pin = pin_entry.get().strip()
        acc_type = account_type.get()
        opening_deposit = deposit_entry.get().strip()

        if not name or not pin or not opening_deposit:
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return

        try:
            float(opening_deposit)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Opening deposit must be a number."
            )
            return

        result, output = run_function_with_input(
            open_account,
            [
                name,
                pin,
                acc_type,
                opening_deposit
            ]
        )

        if result is not False:
            messagebox.showinfo(
                "Account Created",
                output
            )
            window.destroy()
        else:
            messagebox.showerror(
                "Account Creation Failed",
                output
            )

    tk.Button(
        window,
        text="Create Account",
        width=20,
        command=create_account
    ).pack(pady=25)


# ============================================================
# LOGIN
# ============================================================

def login_window():

    window = tk.Toplevel(root)
    window.title("PyBank Login")
    window.geometry("400x350")
    window.resizable(False, False)

    tk.Label(
        window,
        text="PYBANK LOGIN",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        window,
        text="Account Number"
    ).pack()

    account_entry = tk.Entry(
        window,
        width=30
    )
    account_entry.pack(pady=8)

    tk.Label(
        window,
        text="PIN"
    ).pack()

    pin_entry = tk.Entry(
        window,
        width=30,
        show="*"
    )
    pin_entry.pack(pady=8)

    def login_user():

        account_number = account_entry.get().strip()
        pin = pin_entry.get().strip()

        if not account_number or not pin:
            messagebox.showerror(
                "Error",
                "Please enter account number and PIN."
            )
            return

        result, output = run_function_with_input(
            login,
            [
                account_number,
                pin
            ]
        )

        if result:
            messagebox.showinfo(
                "Login Successful",
                "Login successful!"
            )

            window.destroy()

            logged_in_window(result)

        else:
            messagebox.showerror(
                "Login Failed",
                output
            )

    tk.Button(
        window,
        text="Login",
        width=20,
        command=login_user
    ).pack(pady=25)


# ============================================================
# DEPOSIT
# ============================================================

def deposit_window(account_number):

    window = tk.Toplevel(root)
    window.title("Deposit Money")
    window.geometry("400x300")
    window.resizable(False, False)

    tk.Label(
        window,
        text="DEPOSIT MONEY",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        window,
        text="Enter Deposit Amount"
    ).pack()

    amount_entry = tk.Entry(
        window,
        width=30
    )
    amount_entry.pack(pady=10)

    def deposit():

        amount = amount_entry.get().strip()

        if not amount:
            messagebox.showerror(
                "Error",
                "Please enter deposit amount."
            )
            return

        try:
            float(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid amount."
            )
            return

        result, output = run_function_with_input(
            deposit_money,
            [amount],
            account_number
        )

        if result:
            messagebox.showinfo(
                "Deposit Successful",
                output
            )
            window.destroy()
        else:
            messagebox.showerror(
                "Deposit Failed",
                output
            )

    tk.Button(
        window,
        text="Deposit",
        width=20,
        command=deposit
    ).pack(pady=25)


# ============================================================
# WITHDRAW
# ============================================================

def withdraw_window(account_number):

    window = tk.Toplevel(root)
    window.title("Withdraw Money")
    window.geometry("400x300")
    window.resizable(False, False)

    tk.Label(
        window,
        text="WITHDRAW MONEY",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        window,
        text="Enter Withdrawal Amount"
    ).pack()

    amount_entry = tk.Entry(
        window,
        width=30
    )
    amount_entry.pack(pady=10)

    def withdraw():

        amount = amount_entry.get().strip()

        if not amount:
            messagebox.showerror(
                "Error",
                "Please enter withdrawal amount."
            )
            return

        try:
            float(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid amount."
            )
            return

        result, output = run_function_with_input(
            withdraw_money,
            [amount],
            account_number
        )

        if result:
            messagebox.showinfo(
                "Withdrawal Successful",
                output
            )
            window.destroy()
        else:
            messagebox.showerror(
                "Withdrawal Failed",
                output
            )

    tk.Button(
        window,
        text="Withdraw",
        width=20,
        command=withdraw
    ).pack(pady=25)


# ============================================================
# BALANCE
# ============================================================

def balance_window(account_number):

    result, output = run_function_with_input(
        check_balance,
        [],
        account_number
    )

    if result:
        messagebox.showinfo(
            "Account Balance",
            output
        )
    else:
        messagebox.showerror(
            "Balance Enquiry",
            output
        )


# ============================================================
# TRANSACTION HISTORY
# ============================================================

def history_window(account_number):

    result, output = run_function_with_input(
        transaction_history,
        [],
        account_number
    )

    if result:
        messagebox.showinfo(
            "Transaction History",
            output
        )
    else:
        messagebox.showerror(
            "Transaction History",
            output
        )


# ============================================================
# ACCOUNT SUMMARY
# ============================================================

def summary_window(account_number):

    result, output = run_function_with_input(
        account_summary,
        [],
        account_number
    )

    if result:
        messagebox.showinfo(
            "Account Summary",
            output
        )
    else:
        messagebox.showerror(
            "Account Summary",
            output
        )


# ============================================================
# LOGGED-IN MENU
# ============================================================

def logged_in_window(account_number):

    window = tk.Toplevel(root)
    window.title("PyBank - Account Menu")
    window.geometry("500x550")
    window.resizable(False, False)

    tk.Label(
        window,
        text="PYBANK",
        font=("Arial", 22, "bold")
    ).pack(pady=15)

    tk.Label(
        window,
        text="Account Number: " + account_number,
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        window,
        text="ACCOUNT MENU",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        window,
        text="1. Deposit Money",
        width=30,
        command=lambda: deposit_window(account_number)
    ).pack(pady=7)

    tk.Button(
        window,
        text="2. Withdraw Money",
        width=30,
        command=lambda: withdraw_window(account_number)
    ).pack(pady=7)

    tk.Button(
        window,
        text="3. Check Balance",
        width=30,
        command=lambda: balance_window(account_number)
    ).pack(pady=7)

    tk.Button(
        window,
        text="4. Transaction History",
        width=30,
        command=lambda: history_window(account_number)
    ).pack(pady=7)

    tk.Button(
        window,
        text="5. Account Summary",
        width=30,
        command=lambda: summary_window(account_number)
    ).pack(pady=7)

    def logout():

        messagebox.showinfo(
            "Logout",
            "Logged out successfully."
        )

        window.destroy()

    tk.Button(
        window,
        text="6. Logout",
        width=30,
        command=logout
    ).pack(pady=20)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("PyBank")
root.geometry("500x450")
root.resizable(False, False)

tk.Label(
    root,
    text="===================================",
    font=("Arial", 12)
).pack(pady=5)

tk.Label(
    root,
    text="WELCOME TO PYBANK",
    font=("Arial", 22, "bold")
).pack(pady=10)

tk.Label(
    root,
    text="===================================",
    font=("Arial", 12)
).pack(pady=5)

tk.Button(
    root,
    text="1. Open New Account",
    width=30,
    height=2,
    command=open_account_window
).pack(pady=10)

tk.Button(
    root,
    text="2. Login",
    width=30,
    height=2,
    command=login_window
).pack(pady=10)

tk.Button(
    root,
    text="3. Exit",
    width=30,
    height=2,
    command=root.destroy
).pack(pady=10)

root.mainloop()