# Note: The button logic is still bugged, it creates like millions of button
# Note: BUG - holding button will reclick something, even a different button

from game import Game
import pygame
from Button import Button
from game import Game
import random
import math
from network import Network
import pickle
import time
import threading

# Constant
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 1600
HEIGHT = 900
FPS = 60
BUTTON_BORDER_FACTOR = 0.6 # how much button would take up the screen
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
game_input = ""
player_submit = False

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
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1400,750),size= (100,100), text="back",
                           operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
    elif new_status == 3:
        init_game()
    elif new_status == 4:
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1400,750),size= (100,100), text="back",
                           operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
    elif new_status == 5:
        pass
    pygame.time.wait(500) # This function was there to prevent mouse double clicking button / it does not work

def keep_the_game_running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    draw_everything(menu_status)
    game_button_control()
    pygame.display.update()

def init_game():
    # do other thing like mock_client can be done here as well
    global player_submit, game_input, all_button
    net = Network()
    print("you are p"+str(net.player))
    dummy = Game(-1,"dm","dm")
    while True:
        print("hello")
        #print("Wait")
        net.client.send(pickle.dumps(dummy))
        game = net.recv()
        game.dummy = False
        #print(game.ready)
        if game.ready == False:
            print("Waiting for another player")
            keep_the_game_running()
            continue
        # print(game.turn)
        if game.p1_played and game.p2_played:
            game.update_score()
        if str(net.player) == str(game.turn):
            player_submit = False
            print("your turn")
            print(game.numbers_array)
            print(game.sum)
            print(game.equation)
            print(f"P1: {game.p1_score}")
            print(f"P2: {game.p2_score}")
            create_game_button(game.numbers_array)
            while not player_submit:
               keep_the_game_running()
            equation_str = game_input
            print(equation_str)
            if net.player == '1':
                game.p1_played = True
                game.p1_cleared = game.check(equation_str)
                game.turn = 2
            elif net.player == '2':
                game.p2_played = True
                game.p2_cleared = game.check(equation_str)
                game.turn = 1
            net.client.send(pickle.dumps(game))
            print("send " + equation_str)
        else:
            print("waiting for your turn")
            all_button = []
            keep_the_game_running()
        # time.sleep(1)

def user_game_input(button_input):
    global game_input
    if button_input in ALL_ALLOWS_MATH_OP:
        print(f"{button_input}: operation")
    else:
        print(f"{button_input}: numbers")
    game_input = game_input + button_input
    print(f"total input: {game_input}")

def test_reset_button():
    global game_input
    game_input = ""

def test_submit_button():
    global player_submit
    player_submit = True

def game_button_control():
    """function for button control and bug fixes (not yet implemented)"""
    for button in all_button:
        button.update_button()

def randomize_five_number(array):
    length = len(array)
    for i in range(0, length, 1):
        array[i] = random.randint(0,9)

def calculate_button_position(number_of_button, border_factor=BUTTON_BORDER_FACTOR,
                              inline_space=GAME_BUTTON_INLINE_SPACING, offset=0, axis=WIDTH):
    """This function is better used for set of multiple buttons, individual button just set position manually"""
    space_used = border_factor * axis
    button_size = (space_used - ((number_of_button - 1) * inline_space)) / number_of_button
    begining_position = (axis - space_used) / 2
    return button_size, [offset + begining_position + (x * (button_size + inline_space)) for x in range(number_of_button)]

def create_game_button(numbers):
    button_size_y, position_y = calculate_button_position(3, axis=HEIGHT, offset=150, border_factor=0.4) # Hard code : 3 is number of rows
    button_size_x, position_x = calculate_button_position(len(numbers))
    for i in range(len(numbers)):
        button = Button(WIN, DEFAULT_FONT, text=str(numbers[i]), operation=user_game_input,
                        pos=(position_x[i], position_y[0]), size=(button_size_x, button_size_y),
                        button_input=str(numbers[i]))
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(len(ALL_ALLOWS_MATH_OP))

    for i in range(len(ALL_ALLOWS_MATH_OP)):
        button = Button(WIN, DEFAULT_FONT, text=ALL_ALLOWS_MATH_OP[i], operation=user_game_input,
                        pos=(position_x[i], position_y[1]), size=(button_size_x, button_size_y),
                        button_input=ALL_ALLOWS_MATH_OP[i])
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(2)
    reset_button = Button(WIN, DEFAULT_FONT, text="Reset", operation=test_reset_button,
                          pos=(position_x[0], position_y[2]), size=(button_size_x, button_size_y))
    submit_button = Button(WIN, DEFAULT_FONT, text="Submit", operation=test_submit_button,
                           pos=(position_x[1], position_y[2]), size=(button_size_x, button_size_y))
    all_button.append(reset_button)
    all_button.append(submit_button)

def main():
    clock = pygame.time.Clock()
    running = True
    # Create game initial status
    to_mm2_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Play",
                           operation=change_game_status, new_status=2)
    all_button.append(to_mm2_button)
    while running:
        clock.tick(FPS)
        keep_the_game_running()

if __name__ == "__main__":
    main()