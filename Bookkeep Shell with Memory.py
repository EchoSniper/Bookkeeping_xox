#Libraries
import os
import csv
import tkinter as tk
from tkinter import messagebox

# User credentials
USERNAME = "raafiu"
PASSWORD = "raafiu"

# Files for main account
balance_file = "balance.txt"
ledger_file = "ledger.csv"
savings_file = "savings.txt"
savings_ledger = "savings_ledger.csv"

# Init ledger files with headers if not present
def init_ledger(file, header):
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
init_ledger(ledger_file, ["Type", "Amount", "New Balance"])
init_ledger(savings_ledger, ["Type", "Amount", "New Balance"])

# Load Balance Functions 
def load_balance(file):
    return int(open(file).read().strip()) if os.path.exists(file) else 0

def save_balance(file, amount):
    with open(file, "w") as f:
        f.write(str(amount))

# Transaction logging
def log_transaction(file, t_type, amount, balance):
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        sign = "+" if t_type in ["Credit", "Add"] else "-"
        writer.writerow([t_type, f"{sign}BDT {amount}", f"BDT {balance}"])

# Load transaction history
def load_ledger(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        return list(reader)[::-1]

# --- GUI Functions ---
def update_labels():
    balance_label.config(text=f"Main Balance: BDT {main_balance}")
    savings_label.config(text=f"Savings Balance: BDT {savings_balance}")

def update_ledgers():
    ledger_box.delete(1.0, tk.END)
    for row in load_ledger(ledger_file):
        ledger_box.insert(tk.END, f"{row[0]} Amount = {row[2]}\n")

    savings_box.delete(1.0, tk.END)
    for row in load_ledger(savings_ledger):
        savings_box.insert(tk.END, f"{row[0]} Amount = {row[2]}\n")

def handle_transaction(wallet_type, action):
    global main_balance, savings_balance
    try:
        amount = int(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount!")
        return

    if wallet_type == "main":
        if action == "Credit":
            main_balance += amount
        elif action == "Debit":
            if amount > main_balance:
                messagebox.showwarning("Insufficient", "Main account has insufficient funds.")
                return
            main_balance -= amount
        save_balance(balance_file, main_balance)
        log_transaction(ledger_file, action, amount, main_balance)

    elif wallet_type == "savings":
        if action == "Add":
            savings_balance += amount
        elif action == "Withdraw":
            if amount > savings_balance:
                messagebox.showwarning("Insufficient", "Savings account has insufficient funds.")
                return
            savings_balance -= amount
        save_balance(savings_file, savings_balance)
        log_transaction(savings_ledger, action, amount, savings_balance)

    update_labels()
    update_ledgers()
    amount_entry.delete(0, tk.END)

def clear_all_data():
    global main_balance, savings_balance
    if not messagebox.askyesno("Confirm", "Clear all balances and ledgers?"):
        return
    main_balance = 0
    savings_balance = 0
    save_balance(balance_file, main_balance)
    save_balance(savings_file, savings_balance)
    init_ledger(ledger_file, ["Type", "Amount", "New Balance"])
    init_ledger(savings_ledger, ["Type", "Amount", "New Balance"])
    update_labels()
    update_ledgers()
    messagebox.showinfo("Cleared", "All data has been reset.")

# Login window
def show_login():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x200")
    login_win.configure(bg="#f0f0f0")

    tk.Label(login_win, text="Username", bg="#f0f0f0", font=("Arial", 10)).pack(pady=5)
    user_entry = tk.Entry(login_win, font=("Arial", 10))
    user_entry.pack()

    tk.Label(login_win, text="Password", bg="#f0f0f0", font=("Arial", 10)).pack(pady=5)
    pass_entry = tk.Entry(login_win, show="*", font=("Arial", 10))
    pass_entry.pack()

    def try_login():
        if user_entry.get() == USERNAME and pass_entry.get() == PASSWORD:
            login_win.destroy()
            launch_main_ui()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(login_win, text="Login", command=try_login, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=15)

# --- Main UI ---
def launch_main_ui():
    global root, main_balance, savings_balance
    root = tk.Tk()
    root.title("EchoSniper's Homehold Bank Statement")
    root.geometry("800x720")
    root.configure(bg="#e9f5ff")

    # --- Initial Data ---
    main_balance = load_balance(balance_file)
    savings_balance = load_balance(savings_file)

    tk.Label(root, text="EchoSniperXD Banking Dashboard", font=("Arial", 18, "bold"), bg="#e9f5ff", fg="#003366").pack(pady=10)

    global amount_entry, balance_label, savings_label, ledger_box, savings_box

    amount_entry = tk.Entry(root, font=("Arial", 12))
    amount_entry.pack(pady=5)
    amount_entry.insert(0, "Enter Amount")

    balance_label = tk.Label(root, text=f"Main Balance: BDT {main_balance}", font=("Arial", 14), bg="#e9f5ff")
    balance_label.pack(pady=5)

    main_btns = tk.Frame(root, bg="#e9f5ff")
    main_btns.pack()

    tk.Button(main_btns, text="Credit", width=10, bg="#2ecc71", fg="white", font=("Arial", 10), command=lambda: handle_transaction("main", "Credit")).pack(side=tk.LEFT, padx=5)
    tk.Button(main_btns, text="Debit", width=10, bg="#e67e22", fg="white", font=("Arial", 10), command=lambda: handle_transaction("main", "Debit")).pack(side=tk.LEFT, padx=5)

    savings_label = tk.Label(root, text=f"Savings Balance: BDT {savings_balance}", font=("Arial", 14), bg="#e9f5ff")
    savings_label.pack(pady=10)

    savings_btns = tk.Frame(root, bg="#e9f5ff")
    savings_btns.pack()

    tk.Button(savings_btns, text="Add to Savings", width=14, bg="#2980b9", fg="white", font=("Arial", 10), command=lambda: handle_transaction("savings", "Add")).pack(side=tk.LEFT, padx=5)
    tk.Button(savings_btns, text="Withdraw Savings", width=14, bg="#c0392b", fg="white", font=("Arial", 10), command=lambda: handle_transaction("savings", "Withdraw")).pack(side=tk.LEFT, padx=5)

    tk.Button(root, text="Clear All Data", bg="#b30000", fg="white", font=("Arial", 10), width=20, command=clear_all_data).pack(pady=10)

    tk.Label(root, text="Main Account Ledger", font=("Arial", 12, "bold"), bg="#e9f5ff").pack()
    ledger_box = tk.Text(root, height=10, width=95, font=("Arial", 10))
    ledger_box.pack()

    tk.Label(root, text="Savings Ledger", font=("Arial", 12, "bold"), bg="#e9f5ff").pack()
    savings_box = tk.Text(root, height=10, width=95, font=("Arial", 10))
    savings_box.pack()

    update_labels()
    update_ledgers()

    root.mainloop()

# --- Start App ---
show_login()

