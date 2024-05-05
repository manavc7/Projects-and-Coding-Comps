# program that prompts the user for a fraction, formatted as X/Y, wherein each of X and Y is an integer, and then outputs, as a percentage rounded to the nearest integer, how much fuel is in the tank.
# if 1% or less, outputs E, if 99% or more, ouputs F
def main():
    while True:
        try:
            x = input("Fraction: ")
            numerator, denominator = map(int, x.split('/'))
            percentage = int(round(((numerator / denominator) * 100)))
            break
        except ValueError:
            print("Invalid input. Please enter a fraction in the format 'numerator/denominator'.")
        except ZeroDivisionError:
            print("Error: Division by zero.")

    if 100 >= percentage >= 99:
        print("F")
    elif percentage <= 1:
        print("E")
    elif percentage > 100:
        main()
    else:
        print(f"{percentage}%")

main()
