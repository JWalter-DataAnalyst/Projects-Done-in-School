while True:
    conversion = input("Enter your choice between Fahrenheit or Celsius ").upper()

    if conversion == 'F':
        fahrenheit = float(input("Enter the temperature in Fahrenheit: "))
        celsius = (fahrenheit - 32) * 5 / 9
        print("The temperature in Celsius is:", celsius)

    elif conversion == 'C':
        celsius = float(input("Enter the temperature in Celsius "))
        fahrenheit = celsius * 9 / 5 + 32
        print("The temperature in Fahrenheit is:", fahrenheit)
        
    back_to_begining = input("Do you want to perform another conversion? Y/N ").upper()
    if back_to_begining != "Y":
        print("Thank you Goodbye. ")
        break
