# print("For testing purpose")
# print(eval("(2+4)*6/2")==18)

import pygame
import Button

WHITE = (0, 0, 0)

# from game import Game
#
# g1 = Game(1, "MS TEAM", "Taiwan")
# arr, equation, sum = g1.generate_question()
# print("-------------")
# print(arr)
# print(equation)
# print(sum)
# print("-------------")
# print(g1.check(equation, sum+2))

def test_func():
    print("hello func")

pygame.font.init()
WIN = pygame.display.set_mode((800, 600))
BUTTON_FONT1 = pygame.font.SysFont('arial', 69)
running = True
b1 = Button.Button(WIN, BUTTON_FONT1, operation=test_func)
while running:
    WIN.fill(WHITE)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    b1.update_button()
    # b1.draw(mouse)
    # print(mouse)
    # print(b1.is_hovering(mouse))
    pygame.display.update()
