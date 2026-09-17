def show_menu():
    print("Welcome to the calculator!")
    print("Enter an operation choice:")
    print("1: Additon")
    print("2: Subtraction")
    print("3: Multiplication")
    print("4: Division")
    print("5: Quit")

def add():
    print("1: Addition")
    print("Please enter the first number ")
    num1 = input("> ")
    print("Please enter the second number ")
    num2 = input("> ")

    calc = float(num1) + float(num2)
    print("The result is: ", f"{calc:.2f}")

def sub():
    print("2: Subtraction")
    print("Please enter the first number ")
    num1 = input("> ")
    print("Please enter the second number ")
    num2 = input("> ")

    calc = float(num1) - float(num2)
    print("The result is: ", f"{calc:.2f}")

def mult():
    print("3: Multiplication")
    print("Please enter the first number ")
    num1 = input("> ")
    print("Please enter the second number ")
    num2 = input("> ")
    
    calc = float(num1) * float(num2)
    print("The result is: ", f"{calc:.2f}")

def div():
    print("4: Division")
    print("Please enter the first number ")
    num1 = input("> ")
    print("Please enter the second number ")
    num2 = input("> ")
    
    calc = float(num1) / float(num2)
    print("The result is: ", f"{calc:.2f}")

while True:
    show_menu()
    choice = input("> ")

    if choice == "1":
        add()

    elif choice == "2":
        sub()

    elif choice == "3":
        mult()

    elif choice == "4":
        div()

    if choice == "5":
        print("Thank you for using the calculator!")
        break