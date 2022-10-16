# print("For testing purpose")
# print(eval("(2+4)*6/2")==18)

from game import Game

g1 = Game(1, "MS TEAM", "Taiwan")
arr, equation, sum = g1.generate_question()
print("-------------")
print(arr)
print(equation)
print(sum)
print("-------------")
print(g1.check(equation, sum+2))