import math as m
import decimal
from decimal import Decimal

max_decimals = 45

def calculate_pi(n):
    pi = Decimal(m.pi)
    pi_value = str(pi)[:n+2]

    return pi_value



def main():
    while True:
        try:
            n = int(input("How many digits of pi would you like "))
            if n < 0:
                raise ValueError("Input must be non negative")
            if n > max_decimals:
                raise ValueError(f"Input is too large, must be less than {max_decimals}")
            break
        except ValueError as e:
            print(f"Invalid {e}")
        
    print(calculate_pi(n))


if __name__ == "__main__":
    main()