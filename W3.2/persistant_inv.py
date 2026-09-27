import json
from pathlib import Path


inventory = {
    "P100": {
        "name": "Notebook",
        "price": 4.50,
        "quantity": 10
    },
    "P200": {
        "name": "Pen",
        "price": 1.25,
        "quantity": 20
    }
}


FILE_PATH = Path(__file__).parent / "inventory.json"


def load_inventory():
    if not FILE_PATH.exists():
        print("inventory.json not found. Using starting inventory.")
        return inventory

    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Error: inventory.json must contain a JSON object.")
            return None

        return data

    except json.JSONDecodeError:
        print("Error: inventory.json contains malformed JSON.")
        return None


def save_inventory(inventory):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(inventory, file, indent=4)

        print("Inventory saved.")
        return True

    except OSError as error:
        print(f"Error saving inventory: {error}")
        return False


def get_nonnegative_number(prompt, number_type):
    while True:
        value = input(prompt)

        try:
            number = number_type(value)

            if number < 0:
                print("Value cannot be negative.")
            else:
                return number

        except ValueError:
            print("Please enter a valid number.")


def list_products(inventory):
    for product_id, product in inventory.items():
        print(f"{product_id}: {product['name']} - "
              f"${product['price']:.2f} - "
              f"Quantity: {product['quantity']}")


def find_product(inventory, product_id):
    product_id = product_id.strip().upper()

    if product_id == "":
        print("Product ID cannot be blank.")
        return

    if product_id in inventory:
        product = inventory[product_id]
        print(f"{product_id}: {product['name']}")
        print(f"Unit price: ${product['price']:.2f}")
        print(f"Quantity: {product['quantity']}")
    else:
        print("Product not found.")


def update_quantity(inventory, product_id, quantity):
    product_id = product_id.strip().upper()

    if product_id == "":
        print("Product ID cannot be blank.")
        return

    if product_id in inventory:
        inventory[product_id]["quantity"] = quantity
        print("Quantity updated.")
    else:
        print("Product not found.")


def add_product(inventory, product_id, name, price, quantity):
    product_id = product_id.strip().upper()
    name = name.strip()

    if product_id == "":
        print("Product ID cannot be blank.")
        return

    if name == "":
        print("Product name cannot be blank.")
        return

    if product_id in inventory:
        print("Product ID already exists.")
        return

    if price < 0 or quantity < 0:
        print("Price and quantity cannot be negative.")
        return

    inventory[product_id] = {
        "name": name,
        "price": price,
        "quantity": quantity
    }

    print("Product added.")


inventory = load_inventory()

if inventory is None:
    print("Program stopped because the inventory file could not be loaded.")
else:
    while True:
        print("\n1. List products")
        print("2. Find a product")
        print("3. Update quantity")
        print("4. Add a product")
        print("5. Save inventory")
        print("6. Save and quit")

        choice = input("Choose an option: ")

        if choice == "1":
            list_products(inventory)

        elif choice == "2":
            product_id = input("Product ID: ")
            find_product(inventory, product_id)

        elif choice == "3":
            product_id = input("Product ID: ")
            quantity = get_nonnegative_number(
                "New quantity: ",
                int
            )
            update_quantity(inventory, product_id, quantity)

        elif choice == "4":
            product_id = input("Product ID: ")
            name = input("Product name: ")

            price = get_nonnegative_number(
                "Unit price: ",
                float
            )

            quantity = get_nonnegative_number(
                "Quantity: ",
                int
            )

            add_product(
                inventory,
                product_id,
                name,
                price,
                quantity
            )

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            if save_inventory(inventory):
                print("Goodbye!")
                break

        else:
            print("Unknown menu choice.")