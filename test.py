# print("For testing purpose")
# print(eval("(2+4)*6/2")==18)
print("AMOGUS")

### Game object test ###

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


### Button Test ###

# import pygame
# import Button
#
# WHITE = (255, 255, 255)
#
# def test_func(name, number, idk_variable_name_i_guess="bruh"):
#     print(f"hello func {name}, number {number} says \"{idk_variable_name_i_guess}\"")
#
# pygame.font.init()
# WIN = pygame.display.set_mode((800, 600))
# BUTTON_FONT1 = pygame.font.SysFont('arial', 69)
# running = True
# b1 = Button.Button(WIN, BUTTON_FONT1, operation=test_func, pos=(300, 300), text="test", name="tawan", number="28")
# b2 = Button.Button(WIN, BUTTON_FONT1, operation=b1.disable_button, pos=(100, 300), text="dis")
# b3 = Button.Button(WIN, BUTTON_FONT1, operation=b1.enable_button, pos=(500, 300), text="ena")
# WIN.fill(WHITE)
# while running:
#     WIN.fill(WHITE)
#     mouse = pygame.mouse.get_pos()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     b1.update_button()
#     b2.update_button()
#     b3.update_button()
#     # b1.draw(mouse)
#     # print(mouse)
#     # print(b1.is_hovering(mouse))
#     pygame.display.update()
