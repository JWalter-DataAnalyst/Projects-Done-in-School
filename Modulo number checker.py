# Checking for modulo number
numbers_1 = int(input("Hello to use modulo we want to see what is the remainder of any two given numbers looking at what is left after division. Input the first number "))
numbers_2 = int(input("Input the second number "))
modulo_number = numbers_1 % numbers_2

if modulo_number == 0:
    print("Even")
else:
    print(f"Odd {modulo_number}")