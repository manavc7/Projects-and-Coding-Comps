def collatz_steps(n):
    c = 0
    while n != 1:
        if n%2 == 0:
            n /= 2
            c += 1
        else:
            n *= 3
            n += 1
            c += 1

    return c

def main():
    while True:
        try:
            n = int(input("Enter a Number: "))
            if n < 1:
                raise ValueError("Input must be greater than 1")
            break
        except ValueError as e:
            print(f"Invalid {e}")

    print(f" For the number {n} it takes {collatz_steps(n)} steps to reach 1 using the collatz conjecture")

if __name__ == "__main__":
    main()