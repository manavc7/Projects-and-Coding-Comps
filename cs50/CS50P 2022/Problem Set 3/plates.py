def main():
    plate = input("Plate: ")
    plate = plate.strip()
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if two_letters(s) and length(s) and num(s) and disallowed_pass(s):
        return True
    else:
        return False

def two_letters(s):
    return s[:2].isalpha()

def length(s):
    return 2 <= len(s) <= 6

def num(s):
        if not s.isalpha():
            if s[2].isdigit() and s[2] != '0' and s[-1].isdigit():
                for i in range(3,len(s)):
                    if s[i].isalpha():
                        return False

                return True
            elif len(s) > 4:
                if s[3].isdigit() and s[3] != '0' and s[-1].isdigit():
                    for i in range(4,len(s)):
                        if s[i].isalpha():
                            return False

                    return True

                if s[4].isdigit() and s[4] != '0' and s[-1].isdigit():
                    return True
            else:
                return False
        else:
            return True



def disallowed_pass(s):
    invalid_chars = ['.', ' ', ',', ';', ':', '!', '?', "'", '"', '-', '_', '*', '/', '\\', '+', '=', '<', '>', '@', '#', '$', '%', '^', '&', '(', ')', '[', ']', '{', '}', '|']
    for char in s:
        if char in invalid_chars:
            return False
    return True
main()

