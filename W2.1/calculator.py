while True:
    print("Welcome to the calculator!")
    print("Enter an operation choice. (1: Addition, 2: Subtraction, 3: quit)")
    choice = input("> ")

    if choice == "1":
        print("1. Addition")
        print("Please enter the first number ")
        num1 = input("> ")
        print("Please enter the second number ")
        num2 = input("> ")

        calc = float(num1) + float(num2)
        print("The result is: ", f"{calc:.2f}")

    elif choice == "2":
        print("2. Subtraction")
        print("Please enter the first number ")
        num1 = input("> ")
        print("Please enter the second number ")
        num2 = input("> ")

        calc = float(num1) - float(num2)
        print("The result is: ", f"{calc:.2f}")

    if choice == "3":
        print("Thank you for using the calculator!")
        break