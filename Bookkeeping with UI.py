import os
import csv
from datetime import datetime

print("Hello to HomeBankService")
print("This code is written by EchoSniperXD\n")

# Load or initialize balance
balance_file = "balance.txt"
ledger_file = "ledger.csv"

if os.path.exists(balance_file):
    with open(balance_file, "r") as f:
        balance = int(f.read().strip())
    print(f"Loaded Previous Balance: BDT {balance}")
else:
    balance = int(input("Enter your initial amount: BDT "))
    with open(balance_file, "w") as f:
        f.write(str(balance))

# Start transaction loop
while True:
    action = input("\nDo you want to [credit], [debit], or [exit]? ").strip().lower()
    
    if action == "exit":
        break
    
    if action not in ["credit", "debit"]:
        print("Invalid option. Please type 'credit', 'debit', or 'exit'.")
        continue

    amount = int(input(f"Enter amount to {action}: BDT "))

    if action == "credit":
        balance += amount
    elif action == "debit":
        if amount > balance:
            print("❌ Insufficient funds!")
            continue
        balance -= amount

    # Save transaction to ledger
    with open(ledger_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        if os.stat(ledger_file).st_size == 0:
            writer.writerow(["Timestamp", "Type", "Amount", "New Balance"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action.title(), amount, balance])

    # Update balance file
    with open(balance_file, "w") as f:
        f.write(str(balance))

    print(f"✅ {action.title()} successful. New Balance: BDT {balance}")

print("\nGoodbye! Your data has been saved.")

