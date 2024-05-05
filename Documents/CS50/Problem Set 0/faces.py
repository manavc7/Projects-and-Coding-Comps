#program where the user inputs a sentence and any use of :) or :( are replaced by 🙂 or 🙁 respectively
def convert(sentence):
    words = sentence.split()
    emojis = {
        ":)": "🙂",
        ":(": "🙁"
    }

    output = ""
    for word in words:
        output += emojis.get(word, word) + " "
    return output


def main():
    sentence = input("please enter a messsage: ")
    print(convert(sentence))


main()
