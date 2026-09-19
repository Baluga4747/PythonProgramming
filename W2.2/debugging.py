#missing colon after function name.
def greet(name):
    print(f"Hello, {name}!")
 
greet("Alex")

#instead of print it should have been a return to allow additional uses
def add(first, second):
    return first + second
    
answer = add(4, 6)
print(answer * 2)

#need to give the function a global name to be used outside of the function.
def calculate_total(price, quantity):
    total = price * quantity
    return total
 
total = calculate_total(5, 3)
print(total)

#missing a argument in the function call. 
def multiply(first, second):
    return first * second
 
print(multiply(5, 2))