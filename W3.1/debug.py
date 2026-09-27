#added seperator to values
product = {"name": "Notebook", "price": 4.50}
print(product)

#changed number value to 2 due to arrays starting with location 0
products = ["Notebook", "Pen", "Folder"]
print(products[2])

#changed "stock" to "quantity" as stock is not a valid inquerry
product = {"name": "Notebook", "price": 4.50, "quantity": 10}
print(product["quantity"])

#changed the + to a *
product = {"name": "Notebook", "price": 4.50, "quantity": 10}
stock_value = product["price"] * product["quantity"]
print(f"Stock value: ${stock_value:.2f}")