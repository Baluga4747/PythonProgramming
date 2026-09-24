import json
from pathlib import Path

# finding the json file
file_path = Path(__file__).resolve().parent / "product.json"

# open json file
with open(file_path, "r", encoding="utf-8") as file:
    inventory = json.load(file)


while True:
    print("\n1. List products")
    print("2. Add a product")
    print("3. Quit")

    choice = input("Choose an option: ")

    if choice == "1":
        for product_id, product in inventory.items():
            print(f"\nProduct ID: {product_id}")
            print(f"Product: {product['name']}")
            print(f"Unit price: ${product['price']:.2f}")
            print(f"Quantity: {product['quantity']}")

    elif choice == "2":
        product_id = input("Product ID: ").strip().upper()
        name = input("Product name: ").strip()
        price = float(input("Unit price: "))
        quantity = int(input("Quantity: "))

        if product_id in inventory:
            print("Product ID already exists.")
        elif product_id == "":
            print("Product ID cannot be blank.")
        elif name == "":
            print("Product name cannot be blank.")
        elif price < 0 or quantity < 0:
            print("Price and quantity cannot be negative.")
        else:
            inventory[product_id] = {
                "name": name,
                "price": price,
                "quantity": quantity
            }

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(inventory, file, indent=4)

            print("Product added.")

    elif choice == "3":
        break

    else:
        print("Unknown menu choice.")
