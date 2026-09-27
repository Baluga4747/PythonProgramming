# Password Manager

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


def list_passwords():
    print("\nSaved Accounts:")

    for app_name, account in passwords.items():
        print(f"App: {app_name}")
        print(f"Username: {account['username']}")
        print(f"Password: {account['password']}")


def find_password():
    app_name = input("Enter the app name to find: ")

    if app_name in passwords:
        account = passwords[app_name]
        print(f"\nApp: {app_name}")
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

    print("Password saved successfully.")


while True:
    print("\nPassword Manager")
    print("1. List passwords")
    print("2. Find password")
    print("3. Add password")
    print("4. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        list_passwords()

    elif choice == "2":
        find_password()

    elif choice == "3":
        add_password()

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")