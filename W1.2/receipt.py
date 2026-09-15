Item_name = input("What is the name of the item? ")
Item_price = float(input("What is the price of the item? ").replace("$", ""))
Quantity = int(input("How many of the item would you like to purchase? "))
Tax = 0.055

subtotal = Item_price * Quantity
tax_amount = subtotal * Tax
total = subtotal + tax_amount


print(f"Item: {Item_name}")
print(f"Price: ${Item_price:.2f}")
print(f"Quantity: {Quantity}")
print("Receipt;")
print(f"Subtotal: ${subtotal:.2f}")
print(f"Tax: ${tax_amount:.2f}")
print(f"Total: ${total:.2f}")