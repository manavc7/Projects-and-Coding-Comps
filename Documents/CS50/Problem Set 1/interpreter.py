expression = input("Expression: ")
expression = expression.split()

if expression[1] == "+":
    print(float(int(expression[0]) + int(expression[2])))
elif expression[1] == "-":
    print(float(int(expression[0]) - int(expression[2])))
elif expression[1] == "/":
    print(float(int(expression[0]) / int(expression[2])))
elif expression[1] == "*":
    print(float(int(expression[0]) * int(expression[2])))


