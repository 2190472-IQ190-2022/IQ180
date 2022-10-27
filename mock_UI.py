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
# disabled_game_button_index = []
all_button = []
game_input = ""
player_submit = False
user_name = ""

def draw_everything(current_menu_status, to_be_drawn=[]):
    # TO_BE_DRAWN is in [("text", (x, y))] format
    # DONT APPEND THINGS TO BE DRAWN ONTO TO_BE_DRAWN DIRECTLY
    # APPEND THEM ON TO_BE_DRAWN_INTERNAL
    to_be_drawn_internal = []
    WIN.fill(WHITE)
    text_print = ""
    if current_menu_status == 1:
        text_print = "Main menu 1"
        if (user_name,(700,300)) in to_be_drawn:
            to_be_drawn.remove((user_name,(700,300)))
    elif current_menu_status == 2:
        text_print = "Main menu 2"
        rect = pygame.Rect(700,300,200,50)
        color = pygame.Color('lightskyblue1')
        pygame.draw.rect(WIN,color,rect,2)
    elif current_menu_status == 3:
        text_print = "Game"
    elif current_menu_status == 4:
        text_print = "How to play"
        to_be_drawn_internal.append(("this game's trash don't play it", (500, 550)))
    elif current_menu_status == 5:
        text_print = "Setting"
        to_be_drawn_internal.append(("you can change audio, game resolution here (hopefully)", (300, 550)))
    else:
        text_print = "What"
    this_text = DEFAULT_FONT.render(text_print, 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))
    for tbd in to_be_drawn:
        test = DEFAULT_FONT.render(tbd[0], 1, BLACK)
        WIN.blit(test, tbd[1])
    for tbd in to_be_drawn_internal:
        test = DEFAULT_FONT.render(tbd[0], 1, BLACK)
        WIN.blit(test, tbd[1])

def change_game_status(new_status):
    """This function is called when the menu button is pressed (changing user to each menu, mm1, mm2, game, htp, setting)"""
    global menu_status, all_button
    while True:
        if pygame.mouse.get_pressed()[0]:
            keep_the_game_running()
            continue
        else:
            break
    menu_status = new_status
    all_button = []
    button_size_x, position_one_button_x = calculate_button_position(1, border_factor=0.3)
    button_size_y, position_one_button_y = calculate_button_position(1, border_factor=0.1, offset=100, axis=HEIGHT)
    if new_status == 1:
        to_mm2_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Play",
                               operation=change_game_status, new_status=2,
                               pos=(position_one_button_x[0], position_one_button_y[0]),
                               size=(button_size_x, button_size_y))
        all_button.append(to_mm2_button)
        to_setting_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1400,150),size= (100,100), text="SET",
                                   operation=change_game_status, new_status=5)
        to_howtoplay_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1250,150),size= (100,100), text="HTP",
                                     operation=change_game_status, new_status=4)
        all_button.append(to_setting_button)
        all_button.append(to_howtoplay_button)
    elif new_status == 2:
        to_game_button = Button(window=WIN, button_font=DEFAULT_FONT, text="To game",
                                operation=change_game_status, new_status=3,
                                pos=(position_one_button_x[0], position_one_button_y[0]),
                                size=(button_size_x, button_size_y))
        all_button.append(to_game_button)
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1400,750),size= (100,100), text="back",
                                        operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
        enter_name_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(350,300),size= (300,50), text="Enter name",
                                        operation=get_user_name)
        all_button.append(enter_name_button)
    elif new_status == 3:
        init_game()
    elif new_status == 4:
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1400,750),size= (100,100), text="back",
                                        operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
    elif new_status == 5:
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1400,750),size= (100,100), text="back",
                                      operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
    pygame.time.wait(100) # This function was there to prevent mouse double clicking button / it does not work

def keep_the_game_running(things_to_draw=[]):
    """
        This function keep pygame updating and stop it from not responding
        you can also pass something to be drawn in draw_everything function here
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
    draw_everything(menu_status, things_to_draw)
    game_button_control()
    pygame.display.update()
    
def get_user_name(): #get input from user and store in user_name
    global user_name
    typing = True
    while typing:
        things_to_draw = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[0:-1]
                elif event.key == pygame.K_RETURN:
                    typing = False
                    change_game_status(3)
                else:
                    user_name += event.unicode
            things_to_draw.append((user_name,(700,300)))
            draw_everything(menu_status, things_to_draw)
            game_button_control()
            pygame.display.update()
    keep_the_game_running()
                
    
    

def init_game():
    """this is the game"""
    global player_submit, game_input, all_button
    net = Network()
    print("you are p"+str(net.player))
    dummy = Game(-1,"dm","dm")
    while True:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        try:
            net.client.send(pickle.dumps(dummy))
            game = net.recv() # add try except here to prevent server crash
        except:
            change_game_status(new_status=2)
            break
        game.dummy = False
        if game.ready == False:
            #print("Waiting for another player")
            keep_the_game_running()
            continue
        if game.p1_played and game.p2_played:
            game.update_score()
        if str(net.player) == str(game.turn):
            player_submit = False
            game_input = ""
            print("your turn")
            print(game.numbers_array)
            print(game.sum)
            print(game.equation)
            print(f"P1: {game.p1_score}")
            print(f"P2: {game.p2_score}")
            create_game_button(game.numbers_array)
            show_sum(game.sum)
            while not player_submit:
                clock.tick(FPS)
                if math.ceil(60 - (time.time() - game.startTime)) < 0:
                    player_submit = True
                    game_input = ""
                    break
                to_draw = [(f"player 1: {game.p1_score}", (300, 300)),
                           (f"player 2: {game.p2_score}", (600, 300)),
                           (f"time: {math.ceil(60 - (time.time() - game.startTime))}", (900, 300)),
                           (f"input: {game_input}", (1200, 300))]
                keep_the_game_running(things_to_draw=to_draw)

            equation_str = game_input.replace("x", "*").replace("÷", "/")
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
            all_button = []
            clock.tick(FPS)
            keep_the_game_running()
    game_state = []

def user_game_input(button_input, button_index):
    """This the function that is called when user press the button in game session (numbers and operator)"""
    global game_input, disabled_game_button_index
    if button_input in ALL_ALLOWS_MATH_OP:
        print(f"{button_input}: operation")
    else:
        if game_input[len(game_input)-1:].isdigit(): # if last char is number, prevent them to input number
            return
        all_button[button_index].disable_button()
        print(f"{button_input}: numbers")
    game_input = game_input + button_input


def reset_button_operation():
    """This function is called when reset button in the game is pressed"""
    global game_input
    for button in all_button:
        button.enable_button()
    game_input = ""

def submit_button_operation():
    """This function is called when the submit button in the game is pressed"""
    print("submited")
    global player_submit
    player_submit = True
    game_input = ""
    while True:
        if pygame.mouse.get_pressed()[0]:
            keep_the_game_running()
            continue
        else:
            break

def game_button_control():
    """function for button control and bug fixes (not yet implemented)"""
    for button in all_button:
        button.update_button()

def randomize_five_number(array):
    """This function is not used"""
    length = len(array)
    for i in range(0, length, 1):
        array[i] = random.randint(0,9)

def show_sum(sum):
    """Show the expected value from the user's equation"""
    sum_font = pygame.font.SysFont('comicsans', 200)
    button = Button(WIN, sum_font, text=str(sum), operation=None, pos=(WIDTH/2, 150), size=(0, 0),
                    disabled_color=(255, 255, 255))
    all_button.append(button)

def calculate_button_position(number_of_button, border_factor=BUTTON_BORDER_FACTOR,
                              inline_space=GAME_BUTTON_INLINE_SPACING, offset=0, axis=WIDTH):
    """
    This function is used to calculate the position and the size of the button in ONE AXIS (WIDTH or HEIGHT)
    This function is better used for set of multiple buttons, individual button just set position manually
    """
    space_used = border_factor * axis
    button_size = (space_used - ((number_of_button - 1) * inline_space)) / number_of_button
    begining_position = (axis - space_used) / 2
    return button_size, [offset + begining_position + (x * (button_size + inline_space)) for x in range(number_of_button)]

def create_game_button(numbers):
    """This function create game button including numbers and operation"""
    button_size_y, position_y = calculate_button_position(3, axis=HEIGHT, offset=150, border_factor=0.4) # Hard code : 3 is number of rows
    button_size_x, position_x = calculate_button_position(len(numbers))
    for i in range(len(numbers)):
        button = Button(WIN, DEFAULT_FONT, text=str(numbers[i]), operation=user_game_input,
                        pos=(position_x[i], position_y[0]), size=(button_size_x, button_size_y),
                        button_input=str(numbers[i]), button_index=i)
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(len(ALL_ALLOWS_MATH_OP))

    for i in range(len(ALL_ALLOWS_MATH_OP)):
        button = Button(WIN, DEFAULT_FONT, text=ALL_ALLOWS_MATH_OP[i], operation=user_game_input,
                        pos=(position_x[i], position_y[1]), size=(button_size_x, button_size_y),
                        button_input=ALL_ALLOWS_MATH_OP[i], button_index=i)
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(2)
    reset_button = Button(WIN, DEFAULT_FONT, text="Reset", operation=reset_button_operation,
                          pos=(position_x[0], position_y[2]), size=(button_size_x, button_size_y))
    submit_button = Button(WIN, DEFAULT_FONT, text="Submit", operation=submit_button_operation,
                           pos=(position_x[1], position_y[2]), size=(button_size_x, button_size_y))
    all_button.append(reset_button)
    all_button.append(submit_button)

def main():
    """This is the main function"""
    global user_name
    clock = pygame.time.Clock()
    running = True
    button_size_x, position_one_button_x = calculate_button_position(1, border_factor=0.3)
    button_size_y, position_one_button_y = calculate_button_position(1, border_factor=0.1, offset=100, axis=HEIGHT)
    # Create game initial status
    to_mm2_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Play",
                           operation=change_game_status, new_status=2,
                           pos=(position_one_button_x[0], position_one_button_y[0]),
                           size=(button_size_x, button_size_y))
    all_button.append(to_mm2_button)
    to_setting_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1400,150),size= (100,100), text="SET",
                               operation=change_game_status, new_status=5)
    to_howtoplay_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(1250,150),size= (100,100), text="HTP",
                                 operation=change_game_status, new_status=4)
    all_button.append(to_setting_button)
    all_button.append(to_howtoplay_button)
    
    while running:
        clock.tick(FPS)
        keep_the_game_running() 

if __name__ == "__main__":
    main()

print(all_button)