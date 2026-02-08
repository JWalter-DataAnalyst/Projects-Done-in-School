#Tip Calculator
print("Welcome to the tip calculator! ")
bill = float(input("What was the total bill? "))
tip = int(input("How much tip would you like to give 10, 12, or 15? "))
split = int(input("How many people are you splitting with? "))
reaming = round((tip / 100) * bill, 2)
print(f"Each person should pay: {reaming} ")

print("Welcome to the rollarcoaster!")
height = int(input("What is your height in cm? "))

if height >= 120:
    print("You are allowed on the ride, have fun!")
else:
    print("You cannot ride the rollarcoaster")