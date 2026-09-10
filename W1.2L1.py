name = input("What is your name? ")
age = input("What is your age? ")
city = input("What city do you live in? ")
hobby = input("What is your favorite hobby? ")

age = int(age)

hobby_revised = hobby.strip(" ")

print("Name: " + name)

print(f"You are {age} years old and live in {city}.")
print(f"Your favorite hobby is {hobby_revised}.")