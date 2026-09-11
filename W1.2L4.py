#Missing last ")"
name = input("Enter your name: ")
 
print(f"Hello, {name}!")

#age is a string, have to convert to int to do math
age = int(input("Enter your age: "))
 
next_year = age + 1
 
print(f"Next year you will be {next_year}.")

#"cannot convert string to float" error
price = 12
 
price = float(price)
 
print(f"The price is ${price:.2f}.")

#If trying to find total, you multiply price and quantity, not add them together
price = 10.00
quantity = 4
 
total = price * quantity
 
print(f"Total: ${total:.2f}")

#Math was sending all decimals to the right of the decimal point, :.2f forces it to round to 2 decimal places
subtotal = 19.99
tax_rate = 0.055
 
tax = subtotal * tax_rate
total = subtotal + tax
 
print(f"Tax: ${tax:.2f}")
print(f"Total: ${total:.2f}")