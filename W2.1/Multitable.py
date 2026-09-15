#arrays for display
Primary_num = []
mult_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
final_mult = []

while True:
    #ask for input from the user
    print("Enter a number to see the multiplication table for that number ")
    print("Whole numbers only")
    num = input("> ")
    Primary_num.append(num)
    final_mult = [int(num) * i for i in mult_nums]

    #display the multiplication table
    print(f"Multiplication table for {num}:")
    for i in range(len(mult_nums)):
        print(f"{num} x {mult_nums[i]} = {final_mult[i]}")

    #ask if the user wants to see another multiplication table
    again = input("\nWould you like to see another multiplication table? (yes/no): ").lower()

    if again != "yes":
        print("Thank you for using the multiplication table calculator!")
        break