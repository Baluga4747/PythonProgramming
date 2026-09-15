#tip_calculator calculates the tip amount based on the total bill and tip percentage
def tip_calculator():
    bill_amount = float(input("Enter the total bill amount: $"))
    tip_percentage = float(input("Enter the tip percentage (e.g., 15 for 15%): "))
    tip_amount = bill_amount * (tip_percentage / 100)
    total_amount = bill_amount + tip_amount
    print(f"Tip amount: ${tip_amount:.2f}")
    print(f"Total amount (including tip): ${total_amount:.2f}")

#mpg_calculator calculates the miles per gallon based on miles driven and gallons of gas used
def mpg_calculator():
    miles = float(input("How many miles did you drive? "))
    gallons = float(input("How many gallons of gas did you use? "))
    mpg = miles / gallons
    print(f"Your car's fuel efficiency is {mpg} miles per gallon.")

#paycheck_calculator calculates the paycheck amount based on hours worked and hourly rate
def paycheck_calculator():
    hours_worked = float(input("How many hours did you work? "))
    hourly_rate = float(input("What is your hourly rate? "))
    paycheck = hours_worked * hourly_rate
    print(f"Your paycheck amount is: ${paycheck:.2f}")

#temperature_converter converts temperature between Celsius and Fahrenheit
def temperature_converter():
    temperature = float(input("Enter the temperature: "))
    unit = input("Is this in Celsius or Fahrenheit? (C/F): ").lower()
    if unit == "c":
        fahrenheit = (temperature * 9/5) + 32
        print(f"{temperature}°C is equal to {fahrenheit}°F.")
    elif unit == "f":
        celsius = (temperature - 32) * 5/9
        print(f"{temperature}°F is equal to {celsius}°C.")

#hours_to_minutes converts hours to minutes
def hours_to_minutes():
    hours = float(input("Enter the number of hours: "))
    minutes = hours * 60
    print(f"{hours} hours is equal to {minutes} minutes.")

#area_calculator calculates the area of a rectangle based on width and height
def area_calculator():
    width = float(input("Enter the width of the rectangle: "))
    height = float(input("Enter the height of the rectangle: "))
    area = width * height
    print(f"The area of the rectangle is: {area} square units.")

#item_cost_calculator calculates the total cost of an item including tax
def item_cost_calculator():
    price = float(input("Enter the price of the item: $"))
    quantity = int(input("Enter the quantity of the item: "))
    tax_rate = float(input("Enter the tax rate (as a percentage): "))

    subtotal = price * quantity
    tax = subtotal * (tax_rate / 100)
    total = subtotal + tax

    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"Total: ${total:.2f}")

#Start of the main program loop
while True:
    print("Enter a command (type 'exit' to quit and 'Help' for command list):")

    #command line prompt for user input
    command = input("> ").lower()

    if command == "exit":
        print("Goodbye!")
        break

    elif command == "help":
        print("Available commands:")
        print("- exit: Exit the program")
        print("- help: Show this help message")
        print("- Tip: Calculate the tip amount for a bill")
        print("- MPG: Calculate miles per gallon for a trip")
        print("- Paycheck: Calculate your paycheck based on hours worked and hourly rate")
        print("- Temperature: Convert temperature between Celsius and Fahrenheit")
        print("- Hours-to-minutes: Convert hours to minutes")
        print("- Area: Calculate the area of a rectangle")
        print("- Item: Calculate the total cost of an item including tax")

    elif command == "tip":
        tip_calculator()

    elif command == "mpg":
        mpg_calculator()

    elif command == "paycheck":
        paycheck_calculator()

    elif command == "temperature":
        temperature_converter()
        
    elif command == "hours-to-minutes":
        hours_to_minutes()
    
    elif command == "area":
        area_calculator()

    elif command == "item":
        item_cost_calculator()

    else:
        print("Unknown command.")