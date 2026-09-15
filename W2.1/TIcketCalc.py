# ages and prices arrays
ages = []
prices = []

# main command
while True:
    # Clear the arrays for a new calculation
    ages = []
    prices = []

    print("How many tickets would you like to purchase? (enter number value not letters):")

    # command line prompt for user input
    number_tickets = int(input("> "))

    # check if the number of tickets is valid
    if number_tickets > 0:

        for i in range(number_tickets):
            age = int(input("Enter the age of the ticket holder: "))

            if age < 0:
                print("Age cannot be negative. Please enter a valid age.")
                continue

            elif age < 12:
                price = 8.00

            elif age <= 64:
                price = 15.00

            else:
                price = 10.00

            ages.append(age)
            prices.append(price)

            print(f"Ticket price for age {age}: ${price:.2f}")

        # Calculate final total
        total = sum(prices)

        # Display all tickets
        print("\nTickets purchased:")

        for i in range(len(ages)):
            print(f"Age: {ages[i]} | Cost: ${prices[i]:.2f}")

        print(f"\nFinal total: ${total:.2f}")

        # Ask if the user wants another calculation
        again = input("\nWould you like to start another cost calculation? (yes/no): ").lower()

        if again != "yes":
            print("Thank you for using the ticket calculator!")
            break

    else:
        print("Not a valid response. Please enter a number greater than 0.")