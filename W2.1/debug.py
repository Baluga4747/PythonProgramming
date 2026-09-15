#assignment as it is = not ==, fixed to ==
choice = "1"
 
if choice == "1":
    print("Selected option 1")

#forever loop because loop condition is always true, fixed to a condition that can be false
count = 1
while count <= 3:
    print(count)
    count += 1

#program will print first statement due to conditions being met, added 2nd condition to set upper range. 
score = 95
 
if score >= 70 and score < 90:
    print("C")
elif score >= 90:
    print("A")
else:
    print("Below C")

#python stops before the last number in range, aka does not include the last number, fixed to include the last number by adding 1 to the range
for number in range(1, 6):
    print(number)