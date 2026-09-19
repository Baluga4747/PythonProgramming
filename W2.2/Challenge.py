# Functions
def cost():
    print("What is the total for the order?")
    cost_pizzas = float(input("> "))
    return cost_pizzas

def people():
    print("How many people will be eating pizza?")
    num_people = int(input("> "))
    return num_people

def pizza():
    print("How many pizzas will be ordered?")
    num_pizza = int(input("> "))
    return num_pizza

def calcs(cost_pizzas, num_people, num_pizza):
    total_slices = num_pizza * 8
    cost_person = cost_pizzas / num_people
    cost_slice = cost_pizzas / total_slices
    slice_per_person = total_slices / num_people

    print("\n--- Pizza Cost Breakdown ---")
    print(f"Total slices: {total_slices}")
    print(f"Slices per person: {slice_per_person:.2f}")
    print(f"Cost per person: ${cost_person:.2f}")
    print(f"Cost per slice: ${cost_slice:.2f}")


# Data
print("Welcome to the pizza-cost-per-person-splitter!\nPlease enter the required data.")

num_people = people()
num_pizza = pizza()
cost_pizzas = cost()

calcs(cost_pizzas, num_people, num_pizza)