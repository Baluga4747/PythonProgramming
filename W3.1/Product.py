def calculate_stock_value(item):
    return item["price"] * item["quantity"]

name = input("item name: ")

price = float(input("Unit price: "))
while price < 0:
    price = float(input("Unit price cannot be negative. Enter again: "))

quantity = int(input("Quantity: "))
while quantity < 0:
    quantity = int(input("Quantity cannot be negative. Enter again: "))

item = {
    "name": name,
    "price": price,
    "quantity": quantity
}

stock_value = calculate_stock_value(item)

#results
print(f"\nitem: {item['name']}")
print(f"Unit price: ${item['price']:.2f}")
print(f"Quantity: {item['quantity']}")
print(f"Stock value: ${stock_value:.2f}")