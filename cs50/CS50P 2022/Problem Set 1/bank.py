greeting = input("Greeting: ")
greeting = greeting.strip()

if "hello" in greeting.lower():
    print("$0")
elif greeting[0].lower() == "h" and greeting.lower() != "hello":
    print("$20")
else:
    print("$100")
