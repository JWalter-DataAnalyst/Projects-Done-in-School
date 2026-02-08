# print("Welcome to the rollarcoaster!")
height = int(input("What is your height in cm? "))
bill = 0
if height >= 120:
    age = int(input("What is your age? "))
    if age <= 12:
        bill = 5
        print("Child tickets are $5")
    elif age <= 18:
        bill = 7
        print("Youth tickets are $7")
    else:
        bill = 12
        print("Adult tickets are $12")

    want_photos = (input("Do you want a photograph Y for yes and N for no? ")).upper()
    if want_photos == "Y":
        bill += 3
        print(f"Your total bill will be ${bill}")
    else:
        print("Enoy your ride!")

else:
    print("You cannot ride the rollarcoaster.")