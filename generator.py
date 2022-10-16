# Music Lab for generating the equation.

import random

operation = ["+","-","*"] # add, minus, time(multiply)
have_divide = random.getrandbits(1)
numbers_array = []
equation = ""
sum = -1

while True:
    equation = ""
    del numbers_array[:]
    number_of_digits = 4 if have_divide == 1 else 5
    sum = -1
    for i in range(number_of_digits):
        digit = random.randint(1, 9)
        numbers_array.append(digit)
        equation += str(digit)
        if i != number_of_digits-1:
            equation += random.choice(operation)
    sum = eval(equation)
    if sum >= 10:
        break

if have_divide == 1:
    for i in range(9,0,-1):
        if sum%i == 0:
            sum /= i
            sum = int(sum)
            numbers_array.append(i)
            equation = f"({equation})/{str(i)}"
            break


print(equation)
print(eval(equation))
print(sum)
print(numbers_array)

        


