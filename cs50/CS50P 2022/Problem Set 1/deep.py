#program that prompts the user for the answer to the Great Question of Life, the Universe and Everything, outputting Yes if the user inputs 42 or (case-insensitively) forty-two or forty two. Otherwise outputs No
ans = input("What is the Answer to the Great Question of Life, the Universe, and Everything?")

if ans.strip() == "42" or ans.lower() == "forty two" or ans.lower() == "forty-two":
    print("Yes")
else:
    print("No")
