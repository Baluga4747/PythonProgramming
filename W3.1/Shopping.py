Shopping_List = ["Milk", "Eggs", "Bread"]

while True:

    print("Shopping List:")
    for i in range(len(Shopping_List)):
        print(f"- {Shopping_List[i]}")

    item_add = input("Item to add (or type 'done' to quit): ").strip().title()

    if item_add == "Done":
        break

    Shopping_List.append(item_add)

    item_remove = input("Item to remove (or type 'done' to quit): ").strip().title()

    if item_remove == "Done":
        break

    if item_remove in Shopping_List:
        Shopping_List.remove(item_remove)
    else:
        print(f"{item_remove} was not found in the shopping list.")

    print("Updated Shopping List:")
    for i in range(len(Shopping_List)):
        print(f"- {Shopping_List[i]}")

    print()