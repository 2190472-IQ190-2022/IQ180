# Note: The button logic is still bugged, it creates like millions of button
# Note: BUG - holding button will reclick it
from turtle import color
from game import Game
import pygame
from Button import Button
import random

# Constant
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 600
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont('comicsans', 40)
pygame.display.set_caption("IQ1")

# Global Variable
menu_status = 1
# menu status = 1 is mm1, = 2 is mm2, = 3 is game, = 4 is htp, = 5 is setting
all_button = []

def draw_main_menu_1():
    WIN.fill(WHITE)
    this_text = DEFAULT_FONT.render("MM1", 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))

def draw_main_menu_2():
    WIN.fill(WHITE)
    this_text = DEFAULT_FONT.render("MM2", 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))

def draw_setting():
    WIN.fill(WHITE)
    this_text = DEFAULT_FONT.render("Setting", 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))

def draw_how_to_play():
    WIN.fill(WHITE)
    this_text = DEFAULT_FONT.render("How to play", 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))

def draw_game_window():
    WIN.fill(WHITE)
    this_text = DEFAULT_FONT.render("Game", 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))
    display_five_number()

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
        numbers = randomize_five_number([0, 0, 0, 0, 0]) # simulate number array from game object
        create_operation_button()
    elif new_status == 4:
        pass
    elif new_status == 5:
        pass
    pygame.time.wait(300) # This function was there to prevent mouse double clicking button

def test_func(text_test):
    pass

def randomize_five_number(array):
    length = len(array)
    for i in range(0, length, 1):
        array[i] = random.randint(0,9)
    return array

number_set = randomize_five_number([0, 0, 0, 0, 0])
def display_five_number():
    transition_x = 100
    for number in number_set:        
        button = Button(WIN, pygame.font.SysFont('arial', 70), enabled_color=(255, 255, 255), pressed_color=(128, 128, 128), 
                        text=str(number), operation=test_func, text_test=number, pos=(transition_x, 100))
        all_button.append(button)
        transition_x = transition_x + 125

def create_operation_button():
    position_x = 100
    for char in "+-*/()":
        button = Button(WIN, DEFAULT_FONT, text=char, operation=test_func, text_test=char, pos=(position_x, 300))
        all_button.append(button)
        position_x = position_x + 100

def update_operation_button():
    pass

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

        if menu_status == 1:
            draw_main_menu_1()
        elif menu_status == 2:
            draw_main_menu_2()
        elif menu_status == 3:
            draw_game_window()
        elif menu_status == 4:
            draw_how_to_play()
        elif menu_status == 5:
            draw_setting()

        for button in all_button:
            button.update_button()

        pygame.display.update()

if __name__ == "__main__":
    main()