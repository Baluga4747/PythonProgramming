import json
import random
from pathlib import Path

FILE_PATH = Path(__file__).parent / "TruckData.json"

# load data
with FILE_PATH.open("r") as file:
            truck_data = json.load(file)

#random order
current_order = random.choice(truck_data["orders"])


#defintions

    # Validation checks
def get_valid_choice():
    pass

def get_purchase_quantity():
    pass

    #Display
def display_menu():
    print("- - - - - - - - - - M E N U - - - - - - - - - -")
    for menu_id, item in truck_data["menu"].items():
        print(f"  {menu_id}: {item["name"]} - ${item["price"]:.2f}")
    print("- - - - - - - - - - - - - - - - - - - - - - - -")

def display_stock():
    pass

def display_order():
    pass

def display_progress():
    pass

    # Orders
def calculate_order():
    pass

def check_stick():
    pass

def serve_order():
    pass

def decline_order():
    pass

    # save / load
def save_game():
    pass

def load_game():
    pass

def validate_save():
    pass

    # summary
def create_summary ():
    pass

    # Main
def main():
    pass

#main program
display_menu()