text = input("Input: ")

for i in ['A','E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']:
    text = text.replace(i, '')

print(text)
