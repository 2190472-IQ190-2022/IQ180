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
from Popup import Popup
import subprocess
from Animation import Animation
import os
from file_operation import file_operation

# Constant
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 1280
HEIGHT = 720
FPS = 60
BUTTON_BORDER_FACTOR = 0.6 # how much button(s) would take up the screen
SMALL_BUTTON_BORDER_FACTOR = 0.07 # how much one small button would take up the screen
HUD_BORDER_FACTOR = 0.05 # how much of area around the screen element should not enter (use in calculate button position)
GAME_BUTTON_INLINE_SPACING = 10 # how much space between two side-by-side buttons 
GAME_BUTTON_TWOLINE_SPACING = 10 # how much space between two buttons from different line

# display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN_SIZE = pygame.display.set_mode((0, 0), pygame.HIDDEN).get_size()
pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN_SIZE
ALL_ALLOWS_MATH_OP = "+-x÷()"
RESOLUTION_LIST = pygame.display.list_modes()

# BGM
pygame.init()
pygame.mixer.music.load("Sound\BGM.wav")
music_on = False

# fonts
pygame.font.init()
DEFAULT_FONT = pygame.font.Font('Fonts\\pixel_font.ttf', 40)
SMALL_PIXEL_FONT = pygame.font.Font('Fonts\\pixel_font.ttf', 20)
MID_PIXEL_FONT = pygame.font.Font('Fonts\\pixel_font.ttf', 40)
BIG_PIXEL_FONT = pygame.font.Font('Fonts\\pixel_font.ttf', 60)
pygame.display.set_caption("IQ1")

# Global Variable
menu_status = 1 # menu status = 1 is mm1, = 2 is mm2, = 3 is game, = 4 is htp, = 5 is setting
all_button = []
all_popup = []
game_input = ""
player_submit = False
user_name = ""
popup_enable = True
game_full_screen = True
fo = file_operation()

# Images
# test_img = pygame.image.load("C:\\Users\\user\\OneDrive\\Desktop\\Susremaster.webp") # add .convert() to make game faster
# test_img = pygame.transform.scale(test_img, (WIDTH, HEIGHT))
# NOTE: when image is loaded, all of them must be tested. If there's an error, report and replace it with None
# NOTE: I will create a function for testing images later

class Loading_Thread(threading.Thread):

    def __init__(self, target, args):
        threading.Thread.__init__(self, target=target, args=args)
        self.value = None
        
    def run(self):
        try:
            list_of_assets = []
            type = self._args[0]
            path = self._args[1]
            if type == "image":
                self.value = pygame.image.load(path)
            if type == "audio":
                pass
            if type == "images":
                for subpath in os.listdir(path):
                    full_path = os.path.join(path, subpath)
                    if os.path.isfile(full_path): # maybe add file type check here later
                        pic = pygame.image.load(full_path)
                        list_of_assets.append(pic)
                self.value = list_of_assets
            if type == "img_folder":
                pass
            if type == "font":
                pass
        except Exception as e:
            t_obj = []
            t_obj.append(BIG_PIXEL_FONT.render("Error", 1, BLACK))
            t_obj.append(DEFAULT_FONT.render("An exception has occured when loading the following file", 1, BLACK))
            t_obj.append(DEFAULT_FONT.render(f"file type: {type}, file path: {path}", 1, BLACK))
            t_obj.append(DEFAULT_FONT.render("The game will now self destruct in 5 second haha bye", 1, BLACK))
            t_obj.append(SMALL_PIXEL_FONT.render(f"error message: {e}", 1, BLACK))
            all_popup.append(Popup(WIN, text_object=t_obj, duration=5))
            time.sleep(5)
        return None

    def join(self):
        threading.Thread.join(self)
        return self.value

def load_assets(type, file_path): # this function may not be used anymore, already in loading class
    """load asset is BLOCKING, except the process is put into the while loop here"""
    loading_thread = Loading_Thread(None, (type, file_path))
    loading_thread.start()
    loading_popup = Popup(WIN, text_object=[DEFAULT_FONT.render("Loading", 1, BLACK)], allow_click_end=False)
    all_popup.append(loading_popup)

    while loading_thread.is_alive():
        keep_the_game_running()
        loading_popup.extend_time()
    loading_thread.join()
    try:

        all_popup.remove(loading_popup)
    except:
        pass
    
    if loading_thread.value is None:
        exit()

    return loading_thread.value
    

def draw_everything(current_menu_status, to_be_drawn=[]):
    """
        This function can draw it, if you want to draw anything on the window pass it inside to_be_drawn
        to_be_drawn accepts arg in form of [(surface1, (x_pos1, y_pos2)), (surface2, (x_pos2, y_pos2))], etc.
        surface is anything that can be blit'ed, for example, rendered text: rendered_text = FONT.render("hello", 1, WHITE)
        if you want to append draw something from INSIDE this function, append item to to_be_drawn_internal
    """
    to_be_drawn_internal = []
    WIN.fill(WHITE)
    # WIN.blit(test_img, (0,0))
    text_print = ""
    if current_menu_status == 1:
        text_print = "Main menu 1"
        # if (user_name,(700,300)) in to_be_drawn:
        #     to_be_drawn.remove((user_name,(700,300)))
    elif current_menu_status == 2:
        # print(f"{WIDTH}, {HEIGHT}")
        text_print = "Main menu 2"
        rect = pygame.Rect(0.25*WIDTH+310,0.75*HEIGHT,0.3*WIDTH,50)
        color = pygame.Color('lightskyblue1')
        pygame.draw.rect(WIN,color,rect,2)
    elif current_menu_status == 3:
        if len(all_button) == 0:
            text_print = "Waiting for player"
        # else:
        #     pass
    elif current_menu_status == 4:
        text_print = "How to play"
        # to_be_drawn_internal.append(("this game's trash don't play it", (500, 550)))
    elif current_menu_status == 5:
        _, res_buttons_pos_x = calculate_button_position(4, border_factor=0.8, axis=WIDTH)
        _, res_buttons_pos_y = calculate_button_position(1, border_factor=0.1, offset=-0.2*HEIGHT, axis=HEIGHT)
        text_print = "Setting"
        popup_text = "Enabled" if popup_enable else "Disabled"
        popup_status_text = (DEFAULT_FONT.render(f"Popup: {popup_text}", 1, BLACK), (res_buttons_pos_x[0], res_buttons_pos_y[0]+0.15*HEIGHT))
        to_be_drawn_internal.append(popup_status_text)
        # to_be_drawn_internal.append(("you can change audio, game resolution here (hopefully)", (300, 550)))
    else:
        text_print = "What"
    this_text = DEFAULT_FONT.render(text_print, 1, BLACK)
    WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))
    for tbd in to_be_drawn:
        # test = DEFAULT_FONT.render(tbd[0], 1, BLACK)
        WIN.blit(tbd[0], tbd[1])
    for tbd in to_be_drawn_internal:
        # test = DEFAULT_FONT.render(tbd[0], 1, BLACK)
        WIN.blit(tbd[0], tbd[1])

def change_game_status(new_status):
    """This function is called when the menu button is pressed (changing user to each menu, mm1, mm2, game, htp, setting)"""
    global menu_status, all_button, user_name, settings, fo
    if new_status == 3:
        if len(user_name) >= 20:
            all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("name len should be < 20", 1, BLACK)]))
            user_name = ""
            return

    # a = load_assets("images", "Test_Images\\rickroll")

    menu_status = new_status
    all_button = []
    # big button (play game)
    button_size_x, position_one_button_x = calculate_button_position(1, border_factor=0.3, axis=WIDTH)
    button_size_y, position_one_button_y = calculate_button_position(1, border_factor=0.1, offset=0.05*WIDTH, axis=HEIGHT)
    # small button (exit, back, htp, setting)
    small_bsize, _ = calculate_button_position(1, border_factor=SMALL_BUTTON_BORDER_FACTOR, axis=WIDTH)
    _, y_border = calculate_button_position(1, edge_start=True, left_or_top_edge=True)
    y_border = y_border[0]
    if new_status == 1:
        _, three_bpos_x = calculate_button_position(4, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        to_mm2_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Play",
                               operation=change_game_status, new_status=2,
                               pos=(position_one_button_x[0], position_one_button_y[0]),
                               size=(button_size_x, button_size_y))
        all_button.append(to_mm2_button)
        BGM_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(three_bpos_x[0],y_border),size=(small_bsize, small_bsize), text="BGM",
                                    operation=play_BGM)
        to_setting_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(three_bpos_x[1],y_border),size=(small_bsize, small_bsize), text="SET",
                                    operation=change_game_status, new_status=5)
        to_howtoplay_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(three_bpos_x[2],y_border),size=(small_bsize, small_bsize), text="HTP",
                                    operation=change_game_status, new_status=4)
        exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(three_bpos_x[3],y_border),size=(small_bsize, small_bsize), text="GTFO",
                                    operation=exit)
        all_button.append(BGM_button)
        all_button.append(to_setting_button)
        all_button.append(to_howtoplay_button)
        all_button.append(exit_button)
    elif new_status == 2:
        _, two_bpos_x = calculate_button_position(2, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        to_game_button = Button(window=WIN, button_font=DEFAULT_FONT, text="To game",
                                operation=change_game_status, new_status=3,
                                pos=(position_one_button_x[0], position_one_button_y[0]),
                                size=(button_size_x, button_size_y))
        all_button.append(to_game_button)
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(two_bpos_x[0], y_border),
                                    size= (small_bsize, small_bsize), text="back",
                                    operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
        enter_name_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(0.25*WIDTH,0.75*HEIGHT),size= (300,50), text="Enter name",
                                        operation=get_user_name)
        all_button.append(enter_name_button)
        exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(two_bpos_x[1], y_border),
                                    size=(small_bsize, small_bsize), text="GTFO",
                                    operation=exit)
        all_button.append(exit_button)
    elif new_status == 3:
        if len(user_name) == 0:
            user_name = "Player"
        settings['player_name'] = user_name
        fo.save_settings(settings)
        all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render(f"welcome, {user_name}", 1, BLACK)]))
        init_game()
    elif new_status == 4:
        _, one_bpos_x = calculate_button_position(1, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(one_bpos_x[0], y_border),
                                    size= (small_bsize, small_bsize), text="back",
                                    operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
    elif new_status == 5:
        _, one_bpos_x = calculate_button_position(1, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                        pos=(one_bpos_x[0],y_border),
                                        size= (small_bsize, small_bsize), text="back",
                                      operation=change_game_status, new_status=1)
        all_button.append(return_to_mm1_button)
        res_buttons_size_x, res_buttons_pos_x = calculate_button_position(5, border_factor=0.8, axis=WIDTH)
        res_buttons_size_y, res_buttons_pos_y = calculate_button_position(1, border_factor=0.1, offset=-0.2*HEIGHT, axis=HEIGHT)
        res_1_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[0],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[0][0]}x{RESOLUTION_LIST[0][1]}",
                                operation=set_resolution, new_res="0")
        res_2_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[1],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[1][0]}x{RESOLUTION_LIST[1][1]}",
                                operation=set_resolution, new_res="1")
        res_3_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[2],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[2][0]}x{RESOLUTION_LIST[2][1]}",
                                operation=set_resolution, new_res="2")
        res_4_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[3],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[3][0]}x{RESOLUTION_LIST[3][1]}",
                                operation=set_resolution, new_res="3")
        all_button.append(res_1_button)
        all_button.append(res_2_button)
        all_button.append(res_3_button)
        all_button.append(res_4_button)
        if not game_full_screen:
            res_full_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[4],res_buttons_pos_y[0]),
                                    size= (res_buttons_size_x,res_buttons_size_y), text="Full Screen",
                                    operation=set_resolution, new_res="full")
            all_button.append(res_full_button)
        else:
            res_window_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[4],res_buttons_pos_y[0]),
                                    size= (res_buttons_size_x,res_buttons_size_y), text="windowed",
                                    operation=set_resolution, new_res="unfull")
            all_button.append(res_window_button)
        popup_altering_text = "Disable" if popup_enable else "Enable"
        popup_altering_text_reversed = "Enabled" if popup_enable else "Disabled"
        text_width = DEFAULT_FONT.render(f"Popup: {popup_altering_text_reversed}", 1, BLACK).get_width()

        popup_status_button = Button(window=WIN, button_font=DEFAULT_FONT, 
                                    pos=(res_buttons_pos_x[0]+text_width+GAME_BUTTON_INLINE_SPACING, res_buttons_pos_y[0]+0.15*HEIGHT),
                                    size=(res_buttons_size_x, res_buttons_size_y), text=popup_altering_text,
                                    operation=change_popup_status)
        all_button.append(popup_status_button)
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

    # game_button_control()
    for button in all_button:
        button.update_button()

    # game_popup_control()
    for popup in all_popup:
        if popup.get_finish():
            all_popup.remove(popup)
            continue
        if popup_enable:
            popup.draw()

    
    pygame.display.update()
    
def get_user_name(): # get input from user and store in user_name
    global user_name
    typing = True
    while typing:
        things_to_draw = []
        if not menu_status == 2:
            typing = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[0:-1]
                elif event.key == pygame.K_RETURN:
                    typing = False
                    settings['player_name'] = user_name
                    fo.save_settings(settings)
                    change_game_status(3)
                else:
                    user_name += event.unicode
        rendered_user_name = DEFAULT_FONT.render((user_name + "|") if int(time.time()) % 2 == 0 else user_name, 1, BLACK)
        things_to_draw.append((rendered_user_name,(0.25*WIDTH+310,0.75*HEIGHT)))
            # draw_everything(menu_status, things_to_draw)
            # game_button_control()
            # pygame.display.update()
        keep_the_game_running(things_to_draw=things_to_draw) # these 3 lines can be converted to this
        
def play_BGM():
    global music_on, settings, fo
    if not music_on:
        pygame.mixer.music.play(-1)
        music_on = True
        settings["music_on"] = True
        fo.save_settings(settings)
    else:
        pygame.mixer.stop()
        music_on = False
        settings["music_on"] = False
        fo.save_settings(settings)

def init_game():
    """this is the game"""
    global player_submit, game_input, all_button, user_name
    try:
        net = Network()
        print("you are p"+str(net.player))
        dummy = Game(-1,"dm","dm")
        net.client.send(pickle.dumps(dummy))
        game = net.recv()
        game.set_name(net.player,user_name)
        #print(game.p1_name)
        #print(game.p2_name)
        net.client.send(pickle.dumps(game))
    except:
        all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("server error, disconnected", 1, BLACK)]))
        change_game_status(new_status=2)
        return
    
    loop_status = 0
    current_array=[]
    current_sum=0

    while True:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        try:
            net.client.send(pickle.dumps(dummy))
            game = net.recv() # add try except here to prevent server crash
            if game is None:
                raise Exception
        except:
            all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("Error, disconnected", 1, BLACK)]))
            change_game_status(new_status=2)
            break

        if game.ready == False:
            #print("Waiting for another player")
            keep_the_game_running()
            continue
        if game.p1_played and game.p2_played:
            game.update_score()
            try:
                net.client.send(pickle.dumps(game))
            except:
                all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("Error, disconnected", 1, BLACK)]))
                change_game_status(new_status=2)
                break
        if str(net.player) == str(game.turn):
            player_submit = False
            game_input = ""
            print("your turn")
            print(game.start_time)
            print(game.numbers_array)
            print(game.sum)
            print(game.equation)
            print(f"P1: {game.p1_score}")
            print(f"P2: {game.p2_score}")
            current_array=game.numbers_array
            current_sum=game.sum
            create_game_button(game.numbers_array)
            while not player_submit:
                clock.tick(FPS)
                if current_sum!=game.sum or current_array!=game.numbers_array:
                    current_array=game.numbers_array
                    current_sum=game.sum
                    all_button = []
                    create_game_button(game.numbers_array)
                    print("your turn")
                    print(game.start_time)
                    print(game.numbers_array)
                    print(game.sum)
                    print(game.equation)
                    print(f"P1: {game.p1_score}")
                    print(f"P2: {game.p2_score}")
                try:
                    net.client.send(pickle.dumps(dummy))
                    game = net.recv() # add try except here to prevent server crash
                    if game is None:
                        raise Exception
                except:
                    all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("Error, disconnected", 1, BLACK)]))
                    change_game_status(new_status=2)
                    status=2
                    break
                
                if str(net.player) != str(game.turn):
                    loop_status=1
                    break
                if math.ceil(60 - (time.time() - game.start_time)) < 0:
                    game_input = ""
                    break # I think break alone actually work
                sum_font = pygame.font.SysFont('comicsans', 200).render(f"{game.sum}", 1, BLACK)

                to_draw_string = [DEFAULT_FONT.render(f"{game.p1_name}: {game.p1_score}", 1, BLACK),
                                DEFAULT_FONT.render(f"{game.p2_name}: {game.p2_score}", 1, BLACK),
                                DEFAULT_FONT.render(f"time: {math.ceil(60 - (time.time() - game.start_time))}", 1, BLACK),
                                DEFAULT_FONT.render(f"input: {game_input}", 1, BLACK),
                                sum_font                            
                                ]
                to_draw = [(to_draw_string[0], (HUD_BORDER_FACTOR*WIDTH, HUD_BORDER_FACTOR*HEIGHT)),
                           (to_draw_string[1], (HUD_BORDER_FACTOR*WIDTH, HUD_BORDER_FACTOR*HEIGHT+50)),
                           (to_draw_string[2], (WIDTH//2-200, 300)),
                           (to_draw_string[3], (WIDTH//2+200, 300)),
                           (to_draw_string[4], (WIDTH//2-sum_font.get_width()//2, 0))]
                keep_the_game_running(things_to_draw=to_draw)

            equation_str = game_input.replace("x", "*").replace("÷", "/")
            print(equation_str)
            all_button = []

            if loop_status == 1:
                loop_status=0
                continue
            elif loop_status==2:
                loop_status=0
                break

            if net.player == '1':
                game.p1_played = True
                game.p1_cleared = game.check(equation_str)
                game.turn = 2
            elif net.player == '2':
                game.p2_played = True
                game.p2_cleared = game.check(equation_str)
                game.turn = 1
            try:
                net.client.send(pickle.dumps(game))
            except:
                all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("Error, disconnected", 1, BLACK)]))
                change_game_status(new_status=2)
                break
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
            print("pls choose op")
            all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("pls choose op", 1, BLACK)]))
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
    global player_submit
    print("submited")
    player_submit = True
    

def show_sum(sum):
    """Show the expected value from the user's equation"""
    sum_font = pygame.font.SysFont('comicsans', 200)
    button = Button(WIN, sum_font, text=str(sum), operation=None, pos=(WIDTH/2, 150), size=(0, 0),
                    disabled_color=(255, 255, 255))
    all_button.append(button)

def calculate_button_position(number_of_button, border_factor=BUTTON_BORDER_FACTOR,
                              inline_space=GAME_BUTTON_INLINE_SPACING, offset=0, axis=WIDTH, 
                              size=-1, edge_start=False, left_or_top_edge=True):
    """
    This function is used to calculate the position and the size of the button in ONE AXIS (WIDTH or HEIGHT)
    This function is better used for set of multiple buttons, individual button just set position manually
    """
    space_used = 0
    if size == -1:
        space_used = border_factor * axis
    else:
        space_used = (number_of_button * size) + (inline_space * (number_of_button-1))
        
    begining_position = 0
    if not edge_start:
        begining_position = (axis - space_used) / 2
    else:
        if left_or_top_edge:
            begining_position = HUD_BORDER_FACTOR * axis
        else:
            begining_position = begining_position = axis - (HUD_BORDER_FACTOR * axis + space_used)
    button_size = (space_used - ((number_of_button - 1) * inline_space)) / number_of_button
    if size == -1:
        return button_size, [offset + begining_position + (x * (button_size + inline_space)) for x in range(number_of_button)]
    else:
        return size, [offset + begining_position + (x * (size + inline_space)) for x in range(number_of_button)]
        # return size, [offset + begining_position + (x * (button_size + inline_space)) for x in range(number_of_button)]

def create_game_button(numbers):
    """This function create game button including numbers and operation"""
    button_size_y, position_y = calculate_button_position(3, axis=HEIGHT, offset=150, border_factor=0.4) # Hard code : 3 is number of rows
    button_size_x, position_x = calculate_button_position(len(numbers), axis=WIDTH)
    for i in range(len(numbers)):
        button = Button(WIN, DEFAULT_FONT, text=str(numbers[i]), operation=user_game_input,
                        pos=(position_x[i], position_y[0]), size=(button_size_x, button_size_y),
                        button_input=str(numbers[i]), button_index=i)
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(len(ALL_ALLOWS_MATH_OP), axis=WIDTH)

    for i in range(len(ALL_ALLOWS_MATH_OP)):
        button = Button(WIN, DEFAULT_FONT, text=ALL_ALLOWS_MATH_OP[i], operation=user_game_input,
                        pos=(position_x[i], position_y[1]), size=(button_size_x, button_size_y),
                        button_input=ALL_ALLOWS_MATH_OP[i], button_index=i)
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(2, axis=WIDTH)
    reset_button = Button(WIN, DEFAULT_FONT, text="Reset", operation=reset_button_operation,
                          pos=(position_x[0], position_y[2]), size=(button_size_x, button_size_y))
    submit_button = Button(WIN, DEFAULT_FONT, text="Submit", operation=submit_button_operation,
                           pos=(position_x[1], position_y[2]), size=(button_size_x, button_size_y))
    all_button.append(reset_button)
    all_button.append(submit_button)

def set_resolution(new_res):
    global WIDTH, HEIGHT, game_full_screen, settings, fo
    temp_res = WIN.get_size()
    
    if new_res == "0" or new_res == "1" or new_res == '2' or new_res == "3":
        new_res = int(new_res)
        temp_res = RESOLUTION_LIST[new_res][0], RESOLUTION_LIST[new_res][1]
    
    elif new_res == "full":
        game_full_screen = True
        settings["game_full_screen"] = True
    elif new_res == "unfull":
        game_full_screen = False
        settings["game_full_screen"] = False

    if temp_res[0] > SCREEN_SIZE[0] or temp_res[1] > SCREEN_SIZE[1]:
        all_popup.append(Popup(WIN, text_object=[BIG_PIXEL_FONT.render("WARNING", 1, BLACK),
                        SMALL_PIXEL_FONT.render(f"your resolution is terrible", 1, BLACK)]))
        settings["WIDTH"] = SCREEN_SIZE[0]
        settings["HEIGHT"] = SCREEN_SIZE[1]
    else:
        WIDTH, HEIGHT = temp_res
        settings["WIDTH"] = temp_res[0]
        settings["HEIGHT"] = temp_res[1]

    if game_full_screen:
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((WIDTH, HEIGHT))
    fo.save_settings(settings)
    change_game_status(5)
    # print(f"fs: {game_full_screen}, res: {(WIDTH, HEIGHT)}")

def change_popup_status():
    global popup_enable, settings, fo
    popup_enable = not popup_enable
    settings["popup_enable"] = popup_enable
    fo.save_settings(settings)
    change_game_status(5) # refresh page
    # print(popup_enable)

def main():
    """This is the main function"""
    global user_name
    clock = pygame.time.Clock()
    running = True
    change_game_status(1)
    
    while running:
        clock.tick(FPS)
        keep_the_game_running() 

if __name__ == "__main__":
    settings = fo.settings
    WIDTH = settings["WIDTH"]
    HEIGHT = settings["HEIGHT"]
    user_name = settings["player_name"]
    game_full_screen = settings["game_full_screen"]
    popup_enable = settings["popup_enable"]
    music_on = settings["music_on"]
    if music_on:
        pygame.mixer.music.play(-1)
    if game_full_screen:
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((WIDTH, HEIGHT))
    main()

print(all_button)