num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

Op = input("Choose an Op (addition, subtraction, multiplication, division, remainder): ").lower()

if Op == "addition":
    result = num1 + num2
elif Op == "subtraction":
    result = num1 - num2
elif Op == "multiplication":
    result = num1 * num2
elif Op == "division":
    result = num1 / num2
elif Op == "remainder":
    result = num1 % num2
else:
    print("Invalid Op.")
    result = None

if result is not None:
    print("Result:", result)