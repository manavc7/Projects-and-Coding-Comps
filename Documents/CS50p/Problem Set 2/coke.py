#program that prompts the user to insert a coin, one at a time, each time informing the user of the amount due. Once the user has inputted at least 50 cents, output how many cents in change the user is owed assuming that the user will only input integers, and ignore any integer that isn’t an accepted denomination.

due = 50
paid = 0
while paid < due:
    print("Amount Due: " + str(due-paid))
    coin = int(input("Insert Coin: "))
    if coin in [25, 50, 10, 5]:
        paid += coin


print("Change Owed: " + str(paid-due))
