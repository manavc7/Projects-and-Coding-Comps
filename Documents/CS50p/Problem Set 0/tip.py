#program that takes the cost of a meal in dollars and the percentage of tip to leave then outputs the amount to tip in dollars
def main():
    dollars = dollars_to_float(input("How much was the meal? "))
    percent = percent_to_float(input("What percentage would you like to tip? "))
    tip = dollars * percent
    print(f"Leave ${tip:.2f}")


def dollars_to_float(d):
    d = d.replace("$", "")
    output = float(d)
    return output

def percent_to_float(p):
    p = p.replace("%","")

    output = float(float(p)*0.01)
    return output

main()
