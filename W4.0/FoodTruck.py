import json
import random
from pathlib import Path

FILE_PATH = Path(__file__).parent / "TruckData.json"

# Load data
with FILE_PATH.open("r") as file:
    truck_data = json.load(file)

# Game state
current_order_index = 0
current_order = truck_data["orders"][current_order_index]
served = 0
declined = 0
revenue = 0.00 
supply_spending = 0.00
restocks = 3
cash = 100.00

# DEFINITIONS

def get_valid_choice():
    while True:
        choice = input("> ")

        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return choice

        print("Invalid choice. Please enter a number from 1-9.")


def get_purchase_quantity():
    while True:
        quantity = input("Enter quantity to purchase: ")

        if quantity.isdigit() and int(quantity) > 0:
            return int(quantity)

        print("Please enter a positive whole number.")

def display_menu():
    print("- - - - - - - - - - M E N U - - - - - - - - - -")

    for menu_id, item in truck_data["menu"].items():
        print(f"  {menu_id}: {item['name']} - ${item['price']:.2f}")

    print("- - - - - - - - - - - - - - - - - - - - - - - -")


def display_stock():
    print("- - - - - - - - - S T O C K - - - - - - - - -")

    for ingredient_id, ingredient in truck_data["ingredients"].items():
        print(
            f"  {ingredient_id}: "
            f"{ingredient['name']} - "
            f"{ingredient['stock']} in stock"
        )

    print("- - - - - - - - - - - - - - - - - - - - - -")


def display_order():
    print("- - - - - - - - - - O R D E R - - - - - - - - -")

    print(f"Order: {current_order['id']}")

    total = 0

    for menu_id, quantity in current_order["items"].items():
        item = truck_data["menu"][menu_id]

        item_total = item["price"] * quantity
        total += item_total

        print(
            f"  {item['name']} x{quantity} "
            f"- ${item_total:.2f}"
        )

    print(f"Total: ${total:.2f}")
    print("- - - - - - - - - - - - - - - - - - - - - -")


def display_progress():
    print("- - - - - - - - P R O G R E S S - - - - - - - -")

    print(f"Orders served: {served}")
    print(f"Orders declined: {declined}")
    print(f"Orders remaining: {10 - (served + declined)}")
    print(f"Revenue: ${revenue:.2f}")
    print(f"Supply spending: ${supply_spending:.2f}")
    print(f"Restocks remaining: {restocks}")

    print("- - - - - - - - - - - - - - - - - - - - - -")

# Orders

def calculate_order():
    ingredient_needs = {}
    total_price = 0

    for menu_id, quantity in current_order["items"].items():

        menu_item = truck_data["menu"][menu_id]

        total_price += menu_item["price"] * quantity

        for ingredient_id, amount in menu_item["recipe"].items():

            needed = amount * quantity

            if ingredient_id in ingredient_needs:
                ingredient_needs[ingredient_id] += needed
            else:
                ingredient_needs[ingredient_id] = needed

    return ingredient_needs, total_price


def check_stock(ingredient_needs):
    shortages = {}

    for ingredient_id, needed in ingredient_needs.items():

        available = truck_data["ingredients"][ingredient_id]["stock"]

        if available < needed:
            shortages[ingredient_id] = needed - available

    return shortages


def serve_order():
    ingredient_needs, total_price = calculate_order()

    shortages = check_stock(ingredient_needs)

    if shortages:
        print("Not enough ingredients to serve this order.")

        for ingredient_id, shortage in shortages.items():
            ingredient = truck_data["ingredients"][ingredient_id]

            print(
                f"  {ingredient['name']}: "
                f"{shortage} more needed"
            )

        return False

    # Remove ingredients from stock
    for ingredient_id, needed in ingredient_needs.items():
        truck_data["ingredients"][ingredient_id]["stock"] -= needed

    return total_price


def decline_order():
    print("Order declined.")
    return True


# Save / Load

def save_game():
    pass


def load_game():
    pass


def validate_save():
    pass


# Summary

def create_summary():
    pass


# Main

def main():
    pass


# Main program
display_menu()