import csv

def main():

    mail = 0
    spam = 0
    ham = 0

    with open("emails.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mail += 1
            if row["spam"] == "1":
                spam += 1
            else:
                ham += 1

    print(f"mail: {mail}, spam: {spam}, ham: {ham}")


if __name__ == "__main__":
    main()
