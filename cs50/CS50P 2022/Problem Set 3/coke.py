due = 50
paid = 0
while paid < due:
    print("Amount Due: " + str(due-paid))
    coin = int(input("Insert Coin: "))
    if coin in [25, 50, 10, 5]:
        paid += coin


print("Change Owed: " + str(paid-due))
