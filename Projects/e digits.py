import math as m
import decimal
from decimal import Decimal

max_decimals = 45

def calculate_e(n):
    e = Decimal(m.e)
    e_value = str(e)[:n+2]

    return e_value



def main():
    while True:
        try:
            n = int(input("How many digits of e would you like "))
            if n < 0:
                raise ValueError("Input must be non negative")
            if n > max_decimals:
                raise ValueError(f"Input is too large, must be less than {max_decimals}")
            break
        except ValueError as h:
            print(f"Invalid {h}")
        
    print(calculate_e(n))


if __name__ == "__main__":
    main()