# program that prompts the user for a date, anno Domini, in month-day-year order, formatted like 9/8/1636 or September 8, 1636
# then outputs that same date in YYYY-MM-DD format.
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

def main():
    while True:
        try:
            date = input("Date: ")
            if date != date.strip():
                pass
            date = date.strip()

            if ',' in date:
                date = date.replace(",", "")
                date = date.split()
            elif '/' in date:
                date = date.split('/')
                if date[0] in months:
                    continue
            else:
                pass

            if len(date) == 3:
                if date[0] in months:
                    if 32 > int(date[1]) > 0:
                        if len(date[2]) == 4:
                            break
                elif 13 > int(date[0]) > 0:
                    if 32 > int(date[1]) > 0:
                        if len(date[2]) == 4:
                            break
                else:
                    pass
            else:
                pass
        except ValueError:
            pass

    print(conversion(date))

def conversion(date):
    c = 0
    for i in months:
        c += 1
        if i == date[0]:
            date[0] = c

    converted = (f"{str(date[2]).rjust(4,'0')}-{str(date[0]).rjust(2,'0')}-{str(date[1]).rjust(2,'0')}")

    return converted

main()
