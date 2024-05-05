#program that prompts the user for a str of text and then outputs that same text but with all vowels (A, E, I, O, and U) omitted, whether inputted in uppercase or lowercase.
text = input("Input: ")

for i in ['A','E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']:
    text = text.replace(i, '')

print(text)
