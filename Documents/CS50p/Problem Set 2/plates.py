#program that prompts the user for a vanity plate and then output Valid if meets all of the following requirements or Invalid if it does not. 

#“All vanity plates must start with at least two letters.”
#“… vanity plates may contain a maximum of 6 characters (letters or numbers) and a minimum of 2 characters.”
#“Numbers cannot be used in the middle of a plate; they must come at the end. For example, AAA222 would be an acceptable … vanity plate; AAA22A would not be acceptable. The first number used cannot be a ‘0’.”
#“No periods, spaces, or punctuation marks are allowed.”

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

