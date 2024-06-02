#program that prompts the user for the name of a file and then outputs that file’s media type 
file = input("File name: ")
file = file.strip()

if file[-4:].lower() == ".gif":
    print("image/gif")
elif file[-4:].lower() == ".jpg" or file[-5:] == ".jpeg":
    print("image/jpeg")
elif file[-4:].lower() == ".png":
    print("image/png")
elif file[-4:].lower() == ".pdf":
    print("application/pdf")
elif file[-4:].lower() == ".txt":
    print("text/plain")
elif file[-4:].lower() == ".zip":
    print("application/zip")
else:
    print("application/octet-stream")

