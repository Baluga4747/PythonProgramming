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


def list_products(inventory):
    for product_id, product in inventory.items():
        print(f"{product_id}: {product['name']} - "
              f"${product['price']:.2f} - "
              f"Quantity: {product['quantity']}")


def find_product(inventory, product_id):
    product_id = product_id.strip().upper()

    if product_id in inventory:
        product = inventory[product_id]
        print(f"{product_id}: {product['name']}")
        print(f"Unit price: ${product['price']:.2f}")
        print(f"Quantity: {product['quantity']}")
    else:
        print("Product not found.")


def update_quantity(inventory, product_id, quantity):
    product_id = product_id.strip().upper()

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


while True:
    print("\n1. List products")
    print("2. Find a product")
    print("3. Update quantity")
    print("4. Add a product")
    print("5. Quit")

    choice = input("Choose an option: ")

    if choice == "1":
        list_products(inventory)

    elif choice == "2":
        product_id = input("Product ID: ")
        find_product(inventory, product_id)

    elif choice == "3":
        product_id = input("Product ID: ")
        quantity = input("New quantity: ")

        if quantity.isdigit():
            update_quantity(inventory, product_id, int(quantity))
        else:
            print("Please enter a valid quantity.")

    elif choice == "4":
        product_id = input("Product ID: ")
        name = input("Product name: ")
        price = input("Unit price: ")
        quantity = input("Quantity: ")

        try:
            price = float(price)
            quantity = int(quantity)

            add_product(inventory, product_id, name, price, quantity)

        except ValueError:
            print("Please enter valid numbers for price and quantity.")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Unknown menu choice.")