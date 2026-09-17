def build_greeting(name, course):
    return f"Hello, {name}! Welcome to the {course} course."
for i in range(2):
    name = input("Please enter your name: ")
    course = input("Please enter the course you are enrolled in: ")

    print(build_greeting(name, course))