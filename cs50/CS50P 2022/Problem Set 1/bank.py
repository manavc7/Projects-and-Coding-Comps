#program that prompts the user for a greeting. If the greeting starts with “hello”, outputs $0. If the greeting starts with an “h” (but not “hello”), outputs $20. Otherwise, outputs $100
greeting = input("Greeting: ")
greeting = greeting.strip()

if "hello" in greeting.lower():
    print("$0")
elif greeting[0].lower() == "h" and greeting.lower() != "hello":
    print("$20")
else:
    print("$100")
