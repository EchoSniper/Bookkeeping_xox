print("Hello to HomeBankService")
print("This code is written by EchoSniperXD")
balance=int(input("Total Amount You Have: "))
expense=0
num=1
n=input("Do you have any expense?")
while n=="yes":
    expense1=int(input(f"Please Input the Expense Value [{num}]:"))
    num=num+1
    expense=expense+expense1
    n=input("Do you have any other expense?")
print(f"Your Total Expense is {expense}")
current=balance-expense
print(f"Current Balance you have is BDT {current}")
