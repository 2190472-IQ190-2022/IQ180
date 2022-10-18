# Note: The button logic is still bugged, it creates like millions of button
# Note: BUG - holding button will reclick something, even a different button

from game import Game
import pygame
from Button import Button
from game import Game
import random
import math

# Constant
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 1600
HEIGHT = 900
FPS = 60
BUTTON_BORDER_FACTOR = 0.6 # how much button would take up the screen
GAME_BUTTON_YPOS = 400
GAME_BUTTON_INLINE_SPACING = 10 # how much space between two side-by-side buttons
GAME_BUTTON_TWOLINE_SPACING = 10 # how much space between two buttons from different line
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
ALL_ALLOWS_MATH_OP = "+-x÷()"
pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont('comicsans', 40)
pygame.display.set_caption("IQ1")

# Global Variable
menu_status = 1
# menu status = 1 is mm1, = 2 is mm2, = 3 is game, = 4 is htp, = 5 is setting
all_button = []

def draw_everything(current_menu_status):
    WIN.fill(WHITE)
    text_print = ""
    if current_menu_status == 1:
        text_print = "Main menu 1"
    elif current_menu_status == 2:
        text_print = "Main menu 2"
    elif current_menu_status == 3:
        text_print = "Game"
    elif current_menu_status == 4:
        text_print = "How to play"
    elif current_menu_status == 5:
        text_print = "Setting"
    else:
        text_print = "What"
    this_text = DEFAULT_FONT.render(text_print, 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))

def change_game_status(new_status):
    global menu_status, all_button
    # print(menu_status)
    menu_status = new_status
    all_button = []
    if new_status == 1:
        to_mm2_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Play",
                               operation=change_game_status, new_status=2)
        all_button.append(to_mm2_button)
    elif new_status == 2:
        to_game_button = Button(window=WIN, button_font=DEFAULT_FONT, text="To game",
                                operation=change_game_status, new_status=3)
        all_button.append(to_game_button)
    elif new_status == 3:
        create_game_button()
    elif new_status == 4:
        pass
    elif new_status == 5:
        pass
    pygame.time.wait(200) # This function was there to prevent mouse double clicking button

def test_func(text_test):
    print(f"this is test func {text_test}")

def test_reset_button():
    for button in all_button:
        pass

def game_button_control():
    """function for button control and bug fixes (not yet implemented)"""
    for button in all_button:
        button.update_button()

def randomize_five_number(array):
    length = len(array)
    for i in range(0, length, 1):
        array[i] = random.randint(0,9)

def calculate_button_position(number_of_button, border_factor=BUTTON_BORDER_FACTOR,
                              inline_space=GAME_BUTTON_INLINE_SPACING, offset=0):
    """This function is better used for set of multiple buttons, individual button just set position manually"""
    space_used = border_factor * WIDTH
    button_size = (space_used - ((number_of_button - 1) * inline_space)) / number_of_button
    begining_position = (WIDTH - space_used) / 2
    return button_size, [offset + begining_position + (x * (button_size + inline_space)) for x in range(number_of_button)]

def create_game_button():
    numbers = [0, 0, 0, 0, 0]
    position_y = GAME_BUTTON_YPOS
    randomize_five_number(numbers)
    button_size, position_x = calculate_button_position(len(numbers))
    # position_x = begining_position
    for i in range(len(numbers)):
        button = Button(WIN, DEFAULT_FONT, text=str(numbers[i]), operation=test_func,
                        text_test=str(numbers[i]), pos=(position_x[i], position_y),
                        size=(button_size, button_size))
        all_button.append(button)
        # position_x = position_x + button_size + GAME_BUTTON_INLINE_SPACING

    position_y = position_y + button_size + GAME_BUTTON_TWOLINE_SPACING
    button_size, position_x = calculate_button_position(len(ALL_ALLOWS_MATH_OP))
    # position_x = begining_position

    for i in range(len(ALL_ALLOWS_MATH_OP)):
        button = Button(WIN, DEFAULT_FONT, text=ALL_ALLOWS_MATH_OP[i], operation=test_func,
                        text_test=ALL_ALLOWS_MATH_OP[i], pos=(position_x[i], position_y),
                        size=(button_size, button_size))
        all_button.append(button)
        # position_x = position_x + button_size + GAME_BUTTON_INLINE_SPACING

    reset_button = Button(WIN, DEFAULT_FONT, text="Reset", operation=test_reset_button)
    all_button.append(reset_button)

def main():
    clock = pygame.time.Clock()
    running = True
    to_mm2_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Play",
                           operation=change_game_status, new_status=2)
    all_button.append(to_mm2_button)
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_everything(menu_status)
        game_button_control()
        pygame.display.update()


if __name__ == "__main__":
    main()