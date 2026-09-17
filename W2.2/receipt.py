def calc_subtotal(price, quantity):
    return price * quantity

def calc_tax(subtotal, tax_rate):
    return subtotal * tax_rate

def calc_total(subtotal, tax_amount):
    return subtotal + tax_amount



Item_name = input("What is the name of the item? ")
Item_price = float(input("What is the price of the item? ").replace("$", ""))
Quantity = int(input("How many of the item would you like to purchase? "))
Tax = 0.055

subtotal = calc_subtotal(Item_price, Quantity)
tax_amount = calc_tax(subtotal, Tax)
total = calc_total(subtotal, tax_amount)


print(f"Item: {Item_name}")
print(f"Price: ${Item_price:.2f}")
print(f"Quantity: {Quantity}")
print("Receipt;")
print(f"Subtotal: ${subtotal:.2f}")
print(f"Tax: ${tax_amount:.2f}")
print(f"Total: ${total:.2f}")