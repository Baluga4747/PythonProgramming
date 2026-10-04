import json
import random
from pathlib import Path

# FILES
# Set the paths for the game data, save file, and summary file.

#Found a new way to get the path of current file and additional files

BASE_PATH = Path(__file__).parent

DATA_FILE = BASE_PATH / "TruckData.json"
SAVE_FILE = BASE_PATH / "food_truck_save.json"
SUMMARY_FILE = BASE_PATH / "game_summary.txt"

# LOAD TRUCK DATA
# Load the truck information from the JSON file.

with DATA_FILE.open("r") as file:
    truck_data = json.load(file)

# GAME SETTINGS
# Get the main game settings from the truck data.

business_name = truck_data["business_name"]
starting_cash = truck_data["starting_cash"]
restock_limit = truck_data["restock_limit"]

TOTAL_ORDERS = 10

# GAME STATE
# Store the values that change while the game is running.

cash = starting_cash

#global values for later use
revenue = 0.00
supply_spending = 0.00
served = 0
declined = 0

restocks = restock_limit
current_order_index = 0
selected_orders = []
current_order = {}

# INPUT FUNCTIONS
# Get and validate information entered by the player.

def get_valid_choice():
    # Make sure the player chooses a valid menu option.

    while True:
        choice = input("> ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return choice

        print("Invalid choice. Please enter a number from 1-9.")


def get_purchase_quantity():
    # Make sure the player enters a positive quantity.

    while True:
        quantity = input("Enter quantity to purchase: ").strip()
        if quantity.isdigit() and int(quantity) > 0:
            return int(quantity)

        print("Please enter a positive whole number.")

# DISPLAY FUNCTIONS
# Functions that show game information to the player.

def display_menu():
    # Display the menu items and their recipes.

    print("-" * 55)
    print("                 M E N U")
    print("-" * 55)
    for menu_id, item in truck_data["menu"].items():

        print(
            f"{menu_id}: {item['name']} - "
            f"${item['price']:.2f}"
        )

        print("    Recipe:")

        for ingredient_id, amount in item["recipe"].items():
            ingredient_name = truck_data["ingredients"][
                ingredient_id
            ]["name"]
            print(
                f"      {ingredient_name}: {amount}"
            )

    print("-" * 55)

def display_stock():
    # Display ingredient stock, cash, and remaining restocks.

    print("-" * 55)
    print("                 S T O C K")
    print("-" * 55)

    for ingredient_id, ingredient in truck_data["ingredients"].items():
        print(
            f"{ingredient_id}: "
            f"{ingredient['name']} - "
            f"{ingredient['stock']} in stock "
            f"(${ingredient['cost']:.2f} each)"
        )
    print()
    print(f"Cash: ${cash:.2f}")
    print(f"Restocks remaining: {restocks}")
    print("-" * 55)


def calculate_order():
    # Calculate the ingredients and total price needed for the order.

    ingredient_needs = {}
    total_price = 0.00

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

def display_order():
    # Display the items and total price for the current order.

    ingredient_needs, total_price = calculate_order()

    print()
    print("-" * 55)
    print("              C U R R E N T   O R D E R")
    print("-" * 55)

    print(f"Order: {current_order['id']}")

    for menu_id, quantity in current_order["items"].items():
        item = truck_data["menu"][menu_id]
        item_total = item["price"] * quantity
        print(
            f"  {item['name']} x{quantity} "
            f"- ${item_total:.2f}"
        )

    print()
    print(f"Total: ${total_price:.2f}")

    print("-" * 55)

def display_progress():
    # Display the player's progress through the shift.

    completed = served + declined
    remaining = TOTAL_ORDERS - completed

    print()
    print("-" * 55)
    print("               P R O G R E S S")
    print("-" * 55)

    print(f"Orders served:    {served}")
    print(f"Orders declined:  {declined}")
    print(f"Orders remaining: {remaining}")
    print(f"Revenue:          ${revenue:.2f}")
    print(f"Supply spending:  ${supply_spending:.2f}")
    print(f"Restocks left:    {restocks}")
    print(f"Cash:             ${cash:.2f}")

    print("-" * 55)


# ORDER FUNCTIONS
# Functions that check, serve, decline, and move between orders.

def check_stock(ingredient_needs):
    # Check whether there are enough ingredients for the order.

    shortages = {}

    for ingredient_id, needed in ingredient_needs.items():
        available = truck_data["ingredients"][
            ingredient_id
        ]["stock"]
        if available < needed:
            shortages[ingredient_id] = needed - available

    return shortages

def get_random_orders():
    # Select the number of unique orders needed for the game.

    return random.sample(
        truck_data["orders"],
        TOTAL_ORDERS
    )


def advance_order():
    # Move to the next selected customer order.

    global current_order_index
    global current_order

    current_order_index += 1

    if current_order_index < TOTAL_ORDERS:

        current_order = selected_orders[
            current_order_index
        ]

def serve_order():
    # Check stock, remove ingredients, and complete the current order.

    global cash
    global revenue
    global served

    ingredient_needs, total_price = calculate_order()
    shortages = check_stock(ingredient_needs)

    if shortages:

        print()
        print("Not enough ingredients to serve this order.")
        print("Shortages:")
        for ingredient_id, shortage in shortages.items():
            ingredient = truck_data["ingredients"][
                ingredient_id
            ]
            print(
                f"  {ingredient['name']}: "
                f"{shortage} more needed"
            )

        return False


    for ingredient_id, needed in ingredient_needs.items():

        truck_data["ingredients"][
            ingredient_id
        ]["stock"] -= needed

    cash += total_price
    revenue += total_price
    served += 1

    print()
    print(
        f"Order {current_order['id']} served "
        f"for ${total_price:.2f}."
    )

    advance_order()

    return True

def decline_order():
    # Mark the current order as declined and move to the next order.

    global declined

    print()
    print(f"Order {current_order['id']} declined.")

    declined += 1

    advance_order()

# SUPPLY FUNCTIONS
# Functions for purchasing ingredients and managing supplies.

def buy_supplies():
    # Allow the player to purchase ingredients if they have enough cash.

    global cash
    global supply_spending
    global restocks

    if restocks <= 0:

        print()
        print("You have no restocks remaining.")

        return

    print()
    print("-" * 55)
    print("              B U Y   S U P P L I E S")
    print("-" * 55)

    for ingredient_id, ingredient in truck_data[
        "ingredients"
    ].items():

        print(
            f"{ingredient_id}: "
            f"{ingredient['name']} - "
            f"${ingredient['cost']:.2f} each"
        )

    print("-" * 55)

    ingredient_id = input(
        "Enter ingredient ID to purchase: "
    ).strip().upper()

    if ingredient_id not in truck_data["ingredients"]:

        print("Invalid ingredient ID.")

        return

    quantity = get_purchase_quantity()

    ingredient = truck_data["ingredients"][
        ingredient_id
    ]

    cost = ingredient["cost"] * quantity

    print()
    print(
        f"Purchase cost: ${cost:.2f}"
    )

    if cost > cash:

        print(
            f"Not enough cash. "
            f"You need ${cost:.2f}, "
            f"but only have ${cash:.2f}."
        )

        return


    ingredient["stock"] += quantity

    cash -= cost

    supply_spending += cost

    restocks -= 1

    print()
    print(
        f"Purchased {quantity} "
        f"units of {ingredient['name']} "
        f"for ${cost:.2f}."
    )


# SAVE FUNCTIONS
# Functions that save the current game state to a file.

def create_save_data():
    # Create a dictionary containing the information needed to save the game.

    stock_data = {}

    for ingredient_id, ingredient in truck_data[
        "ingredients"
    ].items():

        stock_data[ingredient_id] = ingredient["stock"]

    selected_order_ids = []

    for order in selected_orders:

        selected_order_ids.append(order["id"])

    return {
        "cash": cash,
        "revenue": revenue,
        "supply_spending": supply_spending,
        "served": served,
        "declined": declined,
        "restocks": restocks,
        "current_order_index": current_order_index,
        "selected_orders": selected_order_ids,
        "stock": stock_data
    }


def save_game():
    # Save the current game state as JSON.

    save_data = create_save_data()

    try:

        with SAVE_FILE.open("w") as file:

            json.dump(
                save_data,
                file,
                indent=4
            )

        print()
        print(
            f"Game saved to {SAVE_FILE.name}."
        )

        return True

    except (OSError, TypeError, ValueError) as error:

        print()
        print("Could not save the game.")
        print(f"Error: {error}")

        return False


# LOAD VALIDATION
# Check that saved game data has the correct structure and values.

def validate_save(save_data):
    # Validate the saved data before using it to restore the game.

    if not isinstance(save_data, dict):

        return False

    required_keys = [
        "cash",
        "revenue",
        "supply_spending",
        "served",
        "declined",
        "restocks",
        "current_order_index",
        "selected_orders",
        "stock"
    ]

    for key in required_keys:

        if key not in save_data:

            return False


    for key in [
        "cash",
        "revenue",
        "supply_spending"
    ]:

        value = save_data[key]

        if not isinstance(value, (int, float)):

            return False

        if value < 0:

            return False


    for key in [
        "served",
        "declined",
        "current_order_index"
    ]:

        value = save_data[key]

        if not isinstance(value, int):

            return False

        if value < 0:

            return False


    if not isinstance(
        save_data["selected_orders"],
        list
    ):

        return False

    if len(save_data["selected_orders"]) != TOTAL_ORDERS:

        return False


    valid_order_ids = set()

    for order in truck_data["orders"]:

        valid_order_ids.add(order["id"])

    for order_id in save_data["selected_orders"]:

        if order_id not in valid_order_ids:

            return False


    if save_data["current_order_index"] > TOTAL_ORDERS:

        return False


    if (
        save_data["served"]
        + save_data["declined"]
        != save_data["current_order_index"]
    ):

        return False


    if not isinstance(save_data["restocks"], int):

        return False

    if (
        save_data["restocks"] < 0
        or save_data["restocks"] > restock_limit
    ):

        return False


    if not isinstance(save_data["stock"], dict):

        return False

    for ingredient_id in truck_data["ingredients"]:

        if ingredient_id not in save_data["stock"]:

            return False

        stock = save_data["stock"][ingredient_id]

        if not isinstance(stock, int):

            return False

        if stock < 0:

            return False

    return True


# LOAD GAME
# Restore a previous game from the save file.

def load_game():
    # Load and restore the saved game state.

    global cash
    global revenue
    global supply_spending
    global served
    global declined
    global restocks
    global current_order_index
    global selected_orders
    global current_order

    if not SAVE_FILE.exists():

        print()
        print("No existing save file found.")

        return False

    try:

        with SAVE_FILE.open("r") as file:

            save_data = json.load(file)

    except (OSError, json.JSONDecodeError) as error:

        print()
        print("Could not load the save file.")
        print(f"Error: {error}")
        print("Starting a new game.")

        return False

    if not validate_save(save_data):

        print()
        print("The save file contains invalid data.")
        print("Starting a new game.")

        return False


    cash = float(save_data["cash"])

    revenue = float(save_data["revenue"])

    supply_spending = float(
        save_data["supply_spending"]
    )

    served = save_data["served"]

    declined = save_data["declined"]

    restocks = save_data["restocks"]

    current_order_index = save_data[
        "current_order_index"
    ]


    for ingredient_id, stock in save_data[
        "stock"
    ].items():

        truck_data["ingredients"][
            ingredient_id
        ]["stock"] = stock


    order_lookup = {}

    for order in truck_data["orders"]:

        order_lookup[order["id"]] = order

    selected_orders = []

    for order_id in save_data[
        "selected_orders"
    ]:

        selected_orders.append(
            order_lookup[order_id]
        )


    if current_order_index < TOTAL_ORDERS:

        current_order = selected_orders[
            current_order_index
        ]

    else:

        current_order = {}

    print()
    print("Saved game loaded successfully.")

    return True


# SUMMARY
# Functions that create and save the final shift summary.

def create_summary():
    # Create the final summary of the completed shift.

    ending_cash = cash

    summary = (
        "\n"
        + "=" * 55
        + "\n"
        + f"       {business_name.upper()} - SHIFT COMPLETE\n"
        + "=" * 55
        + "\n\n"
        + "All 10 customer orders have been completed.\n\n"
        + f"Orders served:   {served}\n"
        + f"Orders declined: {declined}\n\n"
        + f"Starting cash:   ${starting_cash:.2f}\n"
        + f"Sales revenue:   ${revenue:.2f}\n"
        + f"Supply spending: ${supply_spending:.2f}\n"
        + f"Ending cash:     ${ending_cash:.2f}\n\n"
        + "=" * 55
    )

    print(summary)

    return summary


def save_summary(summary):
    # Save the final summary to a text file.

    try:

        with SUMMARY_FILE.open("w") as file:

            file.write(summary)

        print()
        print(
            f"Summary saved to {SUMMARY_FILE.name}."
        )

        return True

    except OSError as error:

        print()
        print("Could not write the summary file.")
        print(f"Error: {error}")

        return False


# MAIN GAME
# Run the main game loop and connect all of the game functions.

def main():
    # Start the game and handle the player's actions.

    global selected_orders
    global current_order

    print()
    print("=" * 55)
    print(f"          WELCOME TO THE {business_name.upper()}")
    print("=" * 55)


    loaded = load_game()


    if not loaded:

        print()
        print("Starting a new shift...")

        
        selected_orders = get_random_orders()

        current_order = selected_orders[
            current_order_index
        ]

        print()
        print(
            "10 random customer orders "
            "have been selected."
        )

    # COMPLETED GAME CHECK

    if current_order_index >= TOTAL_ORDERS:

        summary = create_summary()

        save_summary(summary)

        save_game()

        print()
        print("The shift is already complete.")

        return

    # MAIN GAME
# Run the main game loop and connect all of the game functions. LOOP

    while current_order_index < TOTAL_ORDERS:

        print()
        print("=" * 55)

        print(
            f"Order {current_order_index + 1} "
            f"of {TOTAL_ORDERS}"
        )

        print("=" * 55)

        display_order()

        print()
        print("1. View menu and recipes")
        print("2. View stock and cash")
        print("3. Inspect current order")
        print("4. Buy supplies")
        print("5. Serve order")
        print("6. Decline order")
        print("7. View progress")
        print("8. Save game")
        print("9. Save and quit")

        print()
        print("Choose an action:")

        choice = get_valid_choice()

        # VIEW MENU

        if choice == "1":

            display_menu()

        # VIEW STOCK

        elif choice == "2":

            display_stock()

        # VIEW ORDER

        elif choice == "3":

            display_order()

        # BUY SUPPLIES

        elif choice == "4":

            buy_supplies()

        # SERVE ORDER

        elif choice == "5":

            serve_order()

        # DECLINE ORDER

        elif choice == "6":

            decline_order()

        # PROGRESS

        elif choice == "7":

            display_progress()

        # SAVE

        elif choice == "8":

            save_game()

        # SAVE AND QUIT

        elif choice == "9":

            if save_game():

                print()
                print("Game saved. Goodbye!")

                return

    # SHIFT COMPLETE

    print()
    print("All 10 orders have been completed!")

    summary = create_summary()
    save_summary(summary)

    save_game()

    print()
    print("Shift finished. Goodbye!")

# START PROGRAM
# Run the game when this file is opened directly.

if __name__ == "__main__":

    main()
