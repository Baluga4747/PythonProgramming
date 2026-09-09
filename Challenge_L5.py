import random
import string

length = int(input("How long should the password be? "))

if length < 4:
    print("Password must be at least 4 characters long.")
else:
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    characters = string.ascii_letters + string.digits + string.punctuation

    for i in range(length - 4):
        password.append(random.choice(characters))

    random.shuffle(password)

    password = "".join(password)

    print("Your password:", password)