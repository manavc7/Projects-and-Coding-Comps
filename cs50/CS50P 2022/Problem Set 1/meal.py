#program that prompts the user for a time and outputs whether it’s breakfast time, lunch time, or dinner time.
def main():
    time = input("What time is it? ")
    hours = convert(time)

    if 8 >= hours >= 7:
        print("breakfast time")
    elif 13 >= hours >= 12:
        print("lunch time")
    elif 19 >= hours >= 18:
        print("dinner time")


def convert(time):
    if len(time) == 4 :
        a = int(time[0])
        b = float(int(time[2::])/60)
        hours = a+b
        return hours

    if len(time) == 5 :
        a = int(time[0:2])
        b = float(int(time[3::])/60)
        hours = a+b
        return hours



if __name__ == "__main__":
    main()
