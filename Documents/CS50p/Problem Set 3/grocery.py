#program that prompts the user for items, one per line, until the user inputs control-d. Then output the user’s grocery list in all uppercase, sorted alphabetically by item, prefixing each line with the number of times the user inputted that item.

def main():
    groceries = []
    while True:
        try:
            groceries.append(input(""))
        except EOFError:
            break

    uniques = remove_duplicates(groceries)
    for k in uniques:
        print(f"{groceries.count(k)} {k.upper()}")

def remove_duplicates(groceries):
    uniques = []
    for i in groceries:
        if i not in uniques:
            uniques.append(i)

    uniques = sorted(uniques)
    return uniques

main()
