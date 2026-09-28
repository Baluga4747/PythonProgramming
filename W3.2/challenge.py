#Persistant Password Manager
import json
from pathlib import Path

FILE_PATH = Path(__file__).parent / "passwords.json"

passwords = {
    "Google": {
        "username": "example@gmail.com",
        "password": "Example123!"
    },
    "Discord": {
        "username": "example_user",
        "password": "Discord456!"
    },
    "Spotify": {
        "username": "example@email.com",
        "password": "Spotify789!"
    }
}


def load_passwords():
    #Use starting passwords if the file does not exist.
    if not FILE_PATH.exists():
        print("passwords.json not found. Using starting passwords.")
        return passwords

    try:
        with FILE_PATH.open("r") as file:
            loaded_passwords = json.load(file)

        print("Passwords loaded successfully.")
        return loaded_passwords

    except json.JSONDecodeError:
        print("Error: passwords.json contains malformed JSON.")
        print("The existing file was not changed.")
        print("Starting passwords will be used.")
        return passwords

def save_passwords():
    try:
        with FILE_PATH.open("w") as file:
            json.dump(passwords, file, indent=4)

        print("Passwords saved successfully.")

    except OSError:
        print("Error: passwords could not be saved.")


def list_passwords():
    print("Saved Accounts:")

    for app_name, account in passwords.items():
        print(f"App: {app_name}")
        print(f"Username: {account['username']}")
        print(f"Password: {account['password']}")
        print()


def find_password():
    app_name = input("Enter the app name to find: ")

    if app_name in passwords:
        account = passwords[app_name]
        print(f"App: {app_name}")
        print(f"Username: {account['username']}")
        print(f"Password: {account['password']}")
    else:
        print("That app was not found.")


def add_password():
    app_name = input("Enter app name: ")

    if app_name in passwords:
        print("That app already exists.")
        return

    username = input("Enter username: ")
    password = input("Enter password: ")

    passwords[app_name] = {
        "username": username,
        "password": password
    }

    print("Password added successfully.")


def save_and_quit():
    save_passwords()
    print("Goodbye!")


# Load saved passwords before the menu starts.
passwords = load_passwords()


while True:
    print("Password Manager")
    print("1. List passwords")
    print("2. Find password")
    print("3. Add password")
    print("4. Save passwords")
    print("5. Save and quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        list_passwords()

    elif choice == "2":
        find_password()

    elif choice == "3":
        add_password()

    elif choice == "4":
        save_passwords()

    elif choice == "5":
        save_and_quit()
        break

    else:
        print("Invalid choice. Please try again.")