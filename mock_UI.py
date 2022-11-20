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
from Animation import Animation
import os
from file_operation import file_operation

# Constant
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WIDTH = 1280
HEIGHT = 720
FPS = 60
BUTTON_BORDER_FACTOR = 0.5 # how much button(s) would take up the screen
SMALL_BUTTON_BORDER_FACTOR = 0.07 # how much one small button would take up the screen
HUD_BORDER_FACTOR = 0.05 # how much of area around the screen element should not enter (use in calculate button position)
GAME_BUTTON_INLINE_SPACING = 10 # how much space between two side-by-side buttons 
GAME_BUTTON_TWOLINE_SPACING = 10 # how much space between two buttons from different line
SPRITE_SIZE_FACTOR = 10
TILE_POSITION_FACTOR = 0.75
BUTTON_COLOR_ADDITIVE = (128, 128, 128)
CLOUD_SIZE_FACTOR = 0.15
FOREGROUND_SIZE_FACTOR = 0.9
OPTIMUM_RES = (1920, 1080)
# how many pictures are avail??

def make_transparent(image, size, colorkey=BLACK):
    image = pygame.image.load(image)
    image = pygame.transform.scale(image, size)
    image.set_colorkey(colorkey)
    return image.convert()

# display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN_SIZE = pygame.display.set_mode((0, 0), pygame.HIDDEN).get_size()
pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN_SIZE
ALL_ALLOWS_MATH_OP = "+-x÷()"
RESOLUTION_LIST = pygame.display.list_modes()

# tile and background
image_path = os.path.join("Images", "background")
foreground_path = os.path.join("Images", "foreground")
cloud_bw_path = os.path.join("Images", "cloud", "black_and_white")
cloud_path = os.path.join("Images", "cloud", "colored")
image_number = len([entry for entry in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, entry))])
background = pygame.image.load(os.path.join("Images", "background", f"img-{random.randint(0, image_number-1)}.png")).convert()
background_pos = (0, 0)
tile_bw = pygame.image.load(os.path.join("Images", "tile", "jungle_floor_bw.png"))
tile_size = (tile_bw.get_size()[0] * 7, tile_bw.get_size()[1] * 7)
tile_bw = pygame.transform.scale(tile_bw, tile_size)
tile_colored = make_transparent(os.path.join("Images", "tile", "jungle_floor.png"), tile_size)
tile_cont_bw = make_transparent(os.path.join("Images", "tile", "jungle_floor_bw_cont.png"), tile_size)
tile_cont_colored = make_transparent(os.path.join("Images", "tile", "jungle_floor_cont.png"), tile_size)
foreground_number = len([entry for entry in os.listdir(foreground_path)])
cloud_number = len([entry for entry in os.listdir(cloud_path) if os.path.isfile(os.path.join(cloud_path, entry))])
cloud_number_bw = len([entry for entry in os.listdir(cloud_bw_path) if os.path.isfile(os.path.join(cloud_bw_path, entry))])

fade_out = []
fade_out_white = []
for alpha in range(0, 256, 4):
    screen = pygame.Surface((WIDTH, HEIGHT))
    screen.fill(BLACK)
    screen.set_alpha(alpha)
    fade_out.append(screen)

for alpha in range(0, 256, 8):
    screen = pygame.Surface((WIDTH, HEIGHT))
    screen.fill(WHITE)
    screen.set_alpha(alpha)
    fade_out_white.append(screen)

fade_in = fade_out[::-1]
fade_in_white = fade_out_white[::-1]

logo = pygame.transform.scale(pygame.image.load(os.path.join("Images", "logo.jpeg")).convert(), (0.4 * HEIGHT, 0.4 * HEIGHT))
character = pygame.image.load(os.path.join("Images", "character", "character-1.png")).convert()
character_bw = pygame.image.load(os.path.join("Images", "character", "character-1-bw.png")).convert()

character_frame = Animation.create_animation_from_sheet(character, (character.get_width()//8, character.get_height()//3),
                                                        scale_size=(SPRITE_SIZE_FACTOR * (character.get_size()[0] // 8), 
                                                        SPRITE_SIZE_FACTOR * (character.get_size()[1] // 3)), color=BLACK)[16:]
character_frame_bw = Animation.create_animation_from_sheet(character_bw, (character.get_width()//8, character.get_height()//3),
                                                        scale_size=(SPRITE_SIZE_FACTOR * (character.get_size()[0] // 8), 
                                                        SPRITE_SIZE_FACTOR * (character.get_size()[1] // 3)), color=BLACK)[16:]

sprite_pos_y = TILE_POSITION_FACTOR * HEIGHT - SPRITE_SIZE_FACTOR * (character.get_size()[1] / 3) + (1/16 * tile_size[1]) + (1/6 * character.get_height())
character_anime = Animation(WIN, (SPRITE_SIZE_FACTOR * (character.get_size()[0] // 8), SPRITE_SIZE_FACTOR * (character.get_size()[1] // 3)), 
                            (0.15 * WIDTH, sprite_pos_y), 1, (WIDTH, HEIGHT), "char", character_frame, run_every_frame=8)
character_anime_bw = Animation(WIN, (SPRITE_SIZE_FACTOR * (character.get_size()[0] // 8), SPRITE_SIZE_FACTOR * (character.get_size()[1] // 3)), 
                            (0.15 * WIDTH, sprite_pos_y), 1, (WIDTH, HEIGHT), 
                            "char", character_frame_bw, run_every_frame=8)
pet = pygame.image.load(os.path.join("Images", "pet", "img-0.png"))

button_square = pygame.image.load(os.path.join("Images", "button", "square", "img-0.png")).convert()
button_square_brighten = pygame.image.load(os.path.join("Images", "button", "square", "img-0.png")).convert()
button_square_darken = pygame.image.load(os.path.join("Images", "button", "square", "img-0.png")).convert()
button_square_brighten.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_ADD)
button_square_darken.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_SUB)
button_square_bw = pygame.image.load(os.path.join("Images", "button", "square", "img-bw.png")).convert()
button_square_bw_brighten = pygame.image.load(os.path.join("Images", "button", "square", "img-bw.png")).convert()
button_square_bw_darken = pygame.image.load(os.path.join("Images", "button", "square", "img-bw.png")).convert()
button_square_bw_darkest = pygame.image.load(os.path.join("Images", "button", "square", "img-bw.png")).convert()
button_square_bw_brighten.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_ADD)
button_square_bw_darken.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_SUB)
button_square_bw_darkest.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_SUB)
button_rect = pygame.image.load(os.path.join("Images", "button", "rect", "img-0.png")).convert()
button_rect_brighten = pygame.image.load(os.path.join("Images", "button", "rect", "img-0.png")).convert()
button_rect_darken = pygame.image.load(os.path.join("Images", "button", "rect", "img-0.png")).convert()
button_rect_brighten.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_ADD)
button_rect_darken.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_SUB)
button_rect_bw = pygame.image.load(os.path.join("Images", "button", "rect", "img-bw.png")).convert()
button_rect_bw_brighten = pygame.image.load(os.path.join("Images", "button", "rect", "img-bw.png")).convert()
button_rect_bw_darken = pygame.image.load(os.path.join("Images", "button", "rect", "img-bw.png")).convert()
button_rect_bw_darkest = pygame.image.load(os.path.join("Images", "button", "rect", "img-bw.png")).convert()
button_rect_bw_brighten.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_ADD)
button_rect_bw_darken.fill(BUTTON_COLOR_ADDITIVE, special_flags=pygame.BLEND_RGB_SUB)
button_rect_bw_darkest.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_SUB)

# BGM
pygame.init()
pygame.mixer.music.load(os.path.join("Sound", "BGM.wav"))
music_on = True
BGM_volume = 0.5
pygame.mixer.music.play(-1)

# fonts
pygame.font.init()
FONT_PATH = os.path.join("Fonts","pixel_font.ttf")
font_size = [20, 40, 60]
SMALL_PIXEL_FONT = pygame.font.Font(FONT_PATH, font_size[0])
DEFAULT_FONT = pygame.font.Font(FONT_PATH, font_size[1])
# MID_PIXEL_FONT = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), 40)
BIG_PIXEL_FONT = pygame.font.Font(FONT_PATH, font_size[2])
pygame.display.set_caption("IQ1")

# Global Variable
menu_status = 1 # menu status = 1 is mm1, = 2 is mm2, = 3 is game, = 4 is htp, = 5 is setting
all_button = []
all_popup = []
all_animation = []
top_level = []
game_input = ""
player_submit = False
user_name = ""
popup_enable = True
game_full_screen = True
fo = file_operation()

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
                        # pic = pygame.image.load(full_path).convert()
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

def remove_animation_by_ident(ident, rev_all=False):
    removed_all = False
    try:
        while not removed_all:
            for anime in all_animation:
                if anime.get_ident() == ident:
                    all_animation.remove(anime)
                    break
            for anime in top_level:
                if type(anime) == Animation:
                    if anime.get_ident() == ident:
                        top_level.remove(anime)
                        break
            removed_all = True
            for anime in top_level + all_animation:
                if type(anime) == Animation:
                    if anime.get_ident() == ident:
                        removed_all = False
                        break
    except:
        return False

def animation_exist_by_ident(ident):
    for anime in all_animation:
        if anime.get_ident() == ident:
            return True

    return False

def load_assets(type, file_path): # this function may not be used anymore, already in loading class
    """load asset is BLOCKING, except the process is put into the while loop here"""
    loading_thread = Loading_Thread(None, (type, file_path))
    loading_thread.start()
    loading_popup = Popup(WIN, text_object=[DEFAULT_FONT.render("Loading...", 1, BLACK)], allow_click_end=False)
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

def graphic_randomizer():
    """random what graphic assets are being rendered in the back"""
    asset_list = []
    
    # print(foreground_number)
    foreground_index = random.randint(0, foreground_number-1)
    # foreground_index = 5
    foreground_layer_number = len([entry for entry in os.listdir(os.path.join(foreground_path, f"set-{foreground_index}")) if os.path.isfile(os.path.join(foreground_path, f"set-{foreground_index}", entry))])
    speed_foreground_layer = (-2, 0)
    for i in range(foreground_layer_number):
        keep_the_game_running()
        loaded_image = load_assets("image", os.path.join(foreground_path, f"set-{foreground_index}", f"img-{i}.png"))
        loaded_image.set_colorkey(BLACK)
        size_factor = 1
        if foreground_index == 2:
            size_factor = 0.8
            loaded_image.set_colorkey(WHITE)
            loaded_image = pygame.transform.scale(loaded_image, (size_factor * WIDTH, size_factor * HEIGHT)).convert_alpha()
        elif foreground_index == 3:
            loaded_image.set_colorkey(WHITE)
            loaded_image = pygame.transform.scale(loaded_image, (WIDTH, HEIGHT)).convert()
        elif foreground_index == 4 or foreground_index == 5:
            loaded_image.set_colorkey(WHITE)
            size_factor = 0.8
            loaded_image = pygame.transform.scale(loaded_image, (size_factor * WIDTH, size_factor * HEIGHT)).convert_alpha()
        else:
            loaded_image = pygame.transform.scale(loaded_image, (WIDTH, HEIGHT)).convert()

        foreground_anime = Animation(WIN, (size_factor * WIDTH, size_factor * HEIGHT), (0, 0), 1, (WIDTH, HEIGHT), "foreground", [loaded_image], self_replicate=True, speed=speed_foreground_layer)
        # foreground_anime.pause_animation()
        asset_list.append(foreground_anime)

        if foreground_index != 2:
            speed_foreground_layer = (speed_foreground_layer[0] - 0.5, 0)

    # outside this function
    # for every x frame, has y chance start animation
    # return {type and animation obj}
    return asset_list

def draw_everything(current_menu_status, to_be_drawn=[]):
    """
        This function can draw it, if you want to draw anything on the window pass it inside to_be_drawn
        to_be_drawn accepts arg in form of [(surface1, (x_pos1, y_pos2)), (surface2, (x_pos2, y_pos2))], etc.
        surface is anything that can be blit'ed, for example, rendered text: rendered_text = FONT.render("hello", 1, WHITE)
        if you want to append draw something from INSIDE this function, append item to to_be_drawn_internal
    """
    global background_pos

    # print(f"menu: {menu_status}")
    to_be_drawn_internal = []
    # WIN.fill(WHITE)
    # WIN.blit(background, background_pos)
    # background_pos = (background_pos[0]-0.2, background_pos[1])
    text_print = ""
    if current_menu_status == 1:
        # WIN.fill(WHITE)
        text_print = "Main menu 1"
        
    elif current_menu_status == 2:
        # print(f"{WIDTH}, {HEIGHT}")
        # WIN.fill(WHITE)
        text_print = "Main menu 2"
        rect = pygame.Rect(0.25*WIDTH+310,0.75*HEIGHT,0.3*WIDTH,50)
        color = pygame.Color('lightskyblue1')
        pygame.draw.rect(WIN,color,rect,2)

        rect_surface = pygame.Surface((rect.w, rect.h))
        to_be_drawn_internal.append((rect_surface, (0.25*WIDTH+310,0.75*HEIGHT)))
        rendered_user_name = DEFAULT_FONT.render((user_name + "|") if int(time.time()) % 2 == 0 else user_name, 1, WHITE)
        to_be_drawn_internal.append((rendered_user_name, (0.25*WIDTH+310,0.75*HEIGHT)))

    elif current_menu_status == 3:
        # WIN.blit(background, background_pos)
        # background_pos = (background_pos[0]-0.2, background_pos[1])
        if len(all_button) == 0:
            text_print = "Waiting for player"
        # else:
        #     pass
    elif current_menu_status == 4:
        how_to_play = DEFAULT_FONT.render("How to play", 1, BLACK)
        font = pygame.font.Font(FONT_PATH, 30)
        WIN.blit(how_to_play, (WIDTH/2-how_to_play.get_width()/2, 75))
        text_print = "You will be given 5 numbers (1-9), a resulting answer, and 4 operators '+', '-', '*', '/'. "
        text_print += "You must make an equation using all 5 numbers to get the assigned result with the restriction that they have 60 seconds, and only 1 chance. Who answered correctly will get 1 point. "
        text_print += "If both got the answer, it will give the score to the one with shorter time. Otherwise, no score."
        display_how_to_play(WIN, text_print, (0.1*WIDTH, 175), font, BLACK)
    elif current_menu_status == 5:
        # WIN.blit(background, background_pos)
        # background_pos = (background_pos[0]-0.2, background_pos[1])
        _, res_buttons_pos_x = calculate_button_position(4, border_factor=0.8, axis=WIDTH)
        _, res_buttons_pos_y = calculate_button_position(1, border_factor=0.1, offset=-0.2*HEIGHT, axis=HEIGHT)
        text_print = "Setting"
        popup_text = "Enabled" if popup_enable else "Disabled"
        popup_status_text = (DEFAULT_FONT.render(f"Popup: {popup_text}", 1, BLACK), (res_buttons_pos_x[0], res_buttons_pos_y[0]+0.15*HEIGHT))
        BGM_text = "on" if music_on else "off"
        BGM_status_text = (DEFAULT_FONT.render(f"BGM: {BGM_text}", 1, BLACK), (res_buttons_pos_x[0], res_buttons_pos_y[0]+0.3*HEIGHT))
        to_be_drawn_internal.append(popup_status_text)
        to_be_drawn_internal.append(BGM_status_text)
        # to_be_drawn_internal.append(("you can change audio, game resolution here (hopefully)", (300, 550)))
    elif current_menu_status == 6:
        credit = DEFAULT_FONT.render("Credit", 1, BLACK)
        font = pygame.font.Font(FONT_PATH, 30)
        WIN.blit(credit, (WIDTH/2-credit.get_width()/2, 75))
        text_print = ["Krittapasa Boontaveekul 6338006721","Thiti Srikao 6338052521","Russ Choocharn 6338189921"]
        text_print += ["Wuttikorn Nantawitaya 6338206921","Sivakorn Lerttripinyo 6338212621","Supakorn Senlamai 6338216121"]
        offset_y = 0
        for members in text_print:
            member = font.render(members, 1, BLACK)
            display_credit(WIN, members, (WIDTH/2-member.get_width()/2, 175+offset_y), font, BLACK)
            offset_y += 50
    else:
        text_print = "What"
    # this_text = DEFAULT_FONT.render(text_print, 1, BLACK)
    # WIN.blit(this_text, (WIDTH/2-this_text.get_width()/2, HEIGHT/2-this_text.get_height()/2))
    for tbd in to_be_drawn:
        # test = DEFAULT_FONT.render(tbd[0], 1, BLACK)
        WIN.blit(tbd[0], tbd[1])
    for tbd in to_be_drawn_internal:
        # test = DEFAULT_FONT.render(tbd[0], 1, BLACK)
        WIN.blit(tbd[0], tbd[1])

def display_how_to_play(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= 0.9*WIDTH:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height

def display_credit(surface, text, pos, font, color):
    word_surface = font.render(text, True, color)
    surface.blit(word_surface, pos)

def fade_white():
    fade_out_white_anime_obj = Animation(WIN, tile_size, (0, 0), frame=256, screen_size=(WIDTH, HEIGHT), pictures=fade_out_white, 
                                    ident="fade_out_white", speed=(0, 0), rerun=False) 
    top_level.append(fade_out_white_anime_obj)
    fade_out_white_anime_obj.play()
    fade_in_white_anime_obj = Animation(WIN, tile_size, (0, 0), frame=256, screen_size=(WIDTH, HEIGHT), pictures=fade_in_white, 
                                    ident="fade_in_white", speed=(0, 0), rerun=False, hidden=True) 
    fade_in_white_anime_obj.pause_animation()
    top_level.append(fade_in_white_anime_obj)
    while not fade_out_white_anime_obj.get_finish():
        if fade_out_white_anime_obj.get_current_frame() == fade_out_white_anime_obj.get_frame() -1:
            fade_out_white_anime_obj.pause_animation()
            fade_in_white_anime_obj.set_hidden(False)
            fade_in_white_anime_obj.play()
            remove_animation_by_ident("fade_out_white")
            break
        keep_the_game_running()

def make_cloud(black_and_white=True):
    # load all 6 cloud
    # for each cloud random interval, position, size and speed

    c_path = cloud_bw_path
    c_number = cloud_number_bw
    if not black_and_white:
       c_path = cloud_path
       c_number = cloud_number

    for i in range(c_number):
        random_position = random.uniform(0, 0.25)
        random_size_speed = random.uniform(0.5, 0.8)
        # print("loaded " + os.path.join(c_path, f"img-{i}.png"))
        cloud_pic = load_assets("image", os.path.join(c_path, f"img-{i}.png"))
        cloud_pic = pygame.transform.scale(cloud_pic, (random_size_speed * cloud_pic.get_width() * 10, random_size_speed * cloud_pic.get_height() * 10)).convert_alpha()
        cloud_anime = Animation(WIN, (random_size_speed * cloud_pic.get_width() * 10, random_size_speed * cloud_pic.get_height() * 10), pos=(WIDTH, HEIGHT * random_position), frame=1, screen_size=(WIDTH, HEIGHT),
                                    ident="cloud", pictures=[cloud_pic], speed = ((-1+random_size_speed) / 500 * WIDTH, 0))

        cloud_anime.pause_animation()
        all_animation.append(cloud_anime)

def change_game_status(new_status):
    """This function is called when the menu button is pressed (changing user to each menu, mm1, mm2, game, htp, setting)"""
    global menu_status, all_button, user_name, settings, fo

    sprite_pos_y = TILE_POSITION_FACTOR * HEIGHT - SPRITE_SIZE_FACTOR * (character.get_size()[1] / 3) + (1/16 * tile_size[1]) + (1/6 * character.get_height())
    character_frame = None
    # character_anime = None
    tile_type = None

    remove_animation_by_ident("tile")
    remove_animation_by_ident("tile_cont")
    remove_animation_by_ident("logo")
    remove_animation_by_ident("space_background")
    remove_animation_by_ident("char")
    remove_animation_by_ident("foreground", True)
    remove_animation_by_ident("cloud")
    remove_animation_by_ident("pet")

    if new_status == 2 or new_status == 3:
        character_frame = Animation.create_animation_from_sheet(character, (character.get_width()//8, character.get_height()//3),
                                                        scale_size=(SPRITE_SIZE_FACTOR * (character.get_size()[0] // 8), 
                                                        SPRITE_SIZE_FACTOR * (character.get_size()[1] // 3)), color=BLACK)[16:]
        tile_type = (tile_colored, tile_cont_colored)
    else:
        character_frame = Animation.create_animation_from_sheet(character_bw, (character.get_width()//8, character.get_height()//3),
                                                        scale_size=(SPRITE_SIZE_FACTOR * (character.get_size()[0] // 8), 
                                                        SPRITE_SIZE_FACTOR * (character.get_size()[1] // 3)), color=BLACK)[16:]
        tile_type = (tile_bw, tile_cont_bw)

    character_anime = Animation(WIN, (SPRITE_SIZE_FACTOR * (character.get_size()[0] // 8), SPRITE_SIZE_FACTOR * (character.get_size()[1] // 3)), 
                            (0.12 * WIDTH, sprite_pos_y), 1, (WIDTH, HEIGHT), 
                            "char", character_frame, run_every_frame=8, hidden=True)

        
    if not animation_exist_by_ident("tile"):
        all_animation.append(Animation(WIN, tile_size, (0, TILE_POSITION_FACTOR * HEIGHT), frame=1, screen_size=(WIDTH, HEIGHT), pictures=[tile_type[0]], 
                                                ident="tile", speed=(-1, 0), self_replicate=True, hidden=True))
        all_animation.append(Animation(WIN, tile_size, (0, TILE_POSITION_FACTOR * HEIGHT+tile_type[0].get_size()[1]), frame=1, screen_size=(WIDTH, HEIGHT), pictures=[tile_type[1]], 
                                                ident="tile_cont", speed=(-1, 0), self_replicate=True, hidden=True))

    if new_status == 1:
        for i in range(2):
            make_cloud()
    if new_status == 2:
        for i in range(2):
            make_cloud(False)

    if not animation_exist_by_ident("char"):
        all_animation.append(character_anime)

    if new_status == 1 or new_status == 2:
        if not animation_exist_by_ident("logo"):
            logo_anime = Animation(WIN, (0.3 * WIDTH, 0.3 * HEIGHT), (WIDTH//2-logo.get_size()[0]//2, HEIGHT//2-logo.get_size()[1]//2), frame=1, screen_size=(WIDTH, HEIGHT), pictures=[logo], 
                                                ident="logo", speed=(0, 0), self_replicate=False, position_function=(None, math.sin), hidden=True)
            all_animation.append(logo_anime)
        

    all_button = []
    # big button (play game)
    button_size_x, position_one_button_x = calculate_button_position(1, border_factor=0.3, axis=WIDTH)
    button_size_y, position_one_button_y = calculate_button_position(2, border_factor=0.2, offset=0.05*WIDTH, axis=HEIGHT)
    # small button (exit, back, htp, setting)
    small_bsize, _ = calculate_button_position(1, border_factor=SMALL_BUTTON_BORDER_FACTOR, axis=WIDTH)
    _, y_border = calculate_button_position(1, edge_start=True, left_or_top_edge=True)
    y_border = y_border[0]
    if new_status == 1:
        fade_white()

        for anime in all_animation:
            anime.set_hidden(False)

        button_size_five_button, five_button_position  = calculate_button_position(5, border_factor=0.8, axis=WIDTH)
            
        _, three_bpos_x = calculate_button_position(3, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        to_mm2_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Play",
                               operation=change_game_status, new_status=2,
                               pos=(five_button_position[2], ((1+TILE_POSITION_FACTOR)/2) * HEIGHT - button_size_y//2),
                               size=(button_size_five_button, button_size_y), img_mode=True, img_disabled=button_rect_bw_darkest,
                                    img_enabled=button_rect_bw, img_hover=button_rect_bw_brighten, img_pressed=button_rect_bw_darken,)
        all_button.append(to_mm2_button)
        to_credit_button = Button(window=WIN, button_font=DEFAULT_FONT, text="Credit",
                               operation=change_game_status, new_status=6,
                               pos=(five_button_position[1], ((1+TILE_POSITION_FACTOR)/2) * HEIGHT - button_size_y//2),
                               size=(button_size_five_button, button_size_y))
        all_button.append(to_credit_button)
        to_setting_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(five_button_position [0],((1+TILE_POSITION_FACTOR)/2) * HEIGHT - button_size_y//2),
                                    size=(button_size_five_button, button_size_y), text="SET",
                                    operation=change_game_status, new_status=5, img_mode=True, img_disabled=button_square_bw_darkest,
                                    img_enabled=button_square_bw, img_hover=button_square_bw_brighten, img_pressed=button_square_bw_darken,
                                    )
        to_howtoplay_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(five_button_position[3],((1+TILE_POSITION_FACTOR)/2) * HEIGHT - button_size_y//2),
                                    size=(button_size_five_button, button_size_y), text="HTP",
                                    operation=change_game_status, new_status=4, img_mode=True, img_disabled=button_square_bw_darkest,
                                    img_enabled=button_square_bw, img_hover=button_square_bw_brighten, img_pressed=button_square_bw_darken,
                                    )
        exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(five_button_position[4],((1+TILE_POSITION_FACTOR)/2) * HEIGHT - button_size_y//2),
                                    size=(button_size_five_button, button_size_y), text="EXIT",
                                    operation=exit, img_mode=True, img_disabled=button_square_bw_darkest,
                                    img_enabled=button_square_bw, img_hover=button_square_bw_brighten, img_pressed=button_square_bw_darken,
                                    )
        all_button.append(to_setting_button)
        all_button.append(to_howtoplay_button)
        all_button.append(exit_button)

        
    elif new_status == 2:

        fade_white()
        
        for anime in all_animation:
            anime.set_hidden(False)

        keep_the_game_running()
    
        _, two_bpos_x = calculate_button_position(2, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        
        to_game_button = Button(window=WIN, button_font=DEFAULT_FONT, text="To game",
                                operation=change_game_status, new_status=3,
                                pos=(position_one_button_x[0], position_one_button_y[0]),
                                size=(button_size_x, button_size_y), img_mode=True, img_disabled=button_rect_bw,
                                    img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken,)
        all_button.append(to_game_button)
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(two_bpos_x[0], y_border),
                                    size= (small_bsize, small_bsize), text="back",
                                    operation=change_game_status, new_status=1,
                                    img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken,
                                    )
        all_button.append(return_to_mm1_button)
        enter_name_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(0.25*WIDTH,0.75*HEIGHT),size= (300,50), text="Enter name",
                                        operation=get_user_name, img_mode=True, img_disabled=button_rect_bw,
                                    img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken,
                                    )
        all_button.append(enter_name_button)
        exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(two_bpos_x[1], y_border),
                                    size=(small_bsize, small_bsize), text="EXIT",
                                    operation=exit, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken,
                                    )
        all_button.append(exit_button)
        

    elif new_status == 3:
        if len(user_name) == 0:
            user_name = "Player"
        settings['player_name'] = user_name
        fo.save_settings(settings)
        menu_status = new_status

        pet_size = (0.5 * SPRITE_SIZE_FACTOR * (pet.get_size()[0] // 4), 0.5 * (SPRITE_SIZE_FACTOR * (pet.get_size()[1])))
        pet_frame = Animation.create_animation_from_sheet(pet, (pet.get_height(), pet.get_height()), scale_size=pet_size, color=BLACK)
        pet_anime = Animation(WIN, pet_size, (0.07 * WIDTH, sprite_pos_y), 1, (WIDTH, HEIGHT), "pet", pet_frame, position_function=(0, math.sin), run_every_frame=8, hidden=True)
        all_animation.append(pet_anime)
        
        for anime in graphic_randomizer():
            anime.set_hidden(True)
            all_animation.insert(0, anime)

        fade_out_anime_obj = Animation(WIN, size=(WIDTH, HEIGHT), pos=(0, 0), frame=256, screen_size=(WIDTH, HEIGHT), pictures=fade_out, rerun=False, ident="fade_out")
        top_level.append(fade_out_anime_obj)
        
        while not fade_out_anime_obj.get_finish():
            keep_the_game_running()

        for anime in all_animation:
            anime.set_hidden(False)

        top_level.append(Popup(WIN, text_object=[DEFAULT_FONT.render(f"Welcome, {user_name}", 1, BLACK)]))

        if not animation_exist_by_ident("space_background"):
            all_animation.insert(0, Animation(WIN, size=(background.get_width(), background.get_height()), pos=(0, 0), frame=1, screen_size=(WIDTH, HEIGHT),
                                ident="space_background", pictures=[background], speed=(-0.5, 0), self_replicate=True))
        
        _, one_bpos_x = calculate_button_position(2, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(one_bpos_x[1],y_border),size=(small_bsize, small_bsize), text="EXIT",
                                    operation=exit, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken,
                                    )
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT, pos=(one_bpos_x[0],y_border),
                                    size= (small_bsize, small_bsize), text="back",
                                      operation=change_game_status, new_status=2, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken,
                                    )
        all_button.append(return_to_mm1_button)
        all_button.append(exit_button)
        init_game()
        return
    elif new_status == 4 or new_status == 6:
        for anime in all_animation:
            anime.set_hidden(False)
        _, one_bpos_x = calculate_button_position(1, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(one_bpos_x[0], y_border),
                                    size= (small_bsize, small_bsize), text="back",
                                    operation=change_game_status, new_status=1, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken,
                                    )
        all_button.append(return_to_mm1_button)
    elif new_status == 5:
        for anime in all_animation:
            anime.set_hidden(False)
        _, one_bpos_x = calculate_button_position(1, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
        return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                        pos=(one_bpos_x[0],y_border),
                                        size= (small_bsize, small_bsize), text="back",
                                      operation=change_game_status, new_status=1, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
        all_button.append(return_to_mm1_button)
        res_buttons_size_x, res_buttons_pos_x = calculate_button_position(5, border_factor=0.8, axis=WIDTH)
        res_buttons_size_y, res_buttons_pos_y = calculate_button_position(1, border_factor=0.1, offset=-0.2*HEIGHT, axis=HEIGHT)
        res_1_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[0],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[0][0]}x{RESOLUTION_LIST[0][1]}",
                                operation=set_resolution, new_res="0", img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
        res_2_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[1],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[1][0]}x{RESOLUTION_LIST[1][1]}",
                                operation=set_resolution, new_res="1", img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
        res_3_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[2],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[2][0]}x{RESOLUTION_LIST[2][1]}",
                                operation=set_resolution, new_res="2", img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
        res_4_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[3],res_buttons_pos_y[0]),
                                size= (res_buttons_size_x,res_buttons_size_y), text=f"{RESOLUTION_LIST[3][0]}x{RESOLUTION_LIST[3][1]}",
                                operation=set_resolution, new_res="3", img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
        all_button.append(res_1_button)
        all_button.append(res_2_button)
        all_button.append(res_3_button)
        all_button.append(res_4_button)
        if not game_full_screen:
            res_full_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[4],res_buttons_pos_y[0]),
                                    size= (res_buttons_size_x,res_buttons_size_y), text="Full Screen",
                                    operation=set_resolution, new_res="full", img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
            all_button.append(res_full_button)
        else:
            res_window_button = Button(window=WIN, button_font=DEFAULT_FONT,pos=(res_buttons_pos_x[4],res_buttons_pos_y[0]),
                                    size= (res_buttons_size_x,res_buttons_size_y), text="windowed",
                                    operation=set_resolution, new_res="unfull", img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
            all_button.append(res_window_button)
        popup_altering_text = "Disable" if popup_enable else "Enable"
        popup_altering_text_reversed = "Enabled" if popup_enable else "Disabled"
        BGM_altering_text = "off" if music_on else "on"
        BGM_altering_text_reversed = "on" if music_on else "off"
        text_width = DEFAULT_FONT.render(f"Popup: {popup_altering_text_reversed}", 1, BLACK).get_width()
        text_width_BGM = DEFAULT_FONT.render(f"BGM: {BGM_altering_text_reversed}", 1, BLACK).get_width()
        popup_status_button = Button(window=WIN, button_font=DEFAULT_FONT, 
                                    pos=(res_buttons_pos_x[0]+text_width+GAME_BUTTON_INLINE_SPACING, res_buttons_pos_y[0]+0.15*HEIGHT),
                                    size=(res_buttons_size_x, res_buttons_size_y), text=popup_altering_text,
                                    operation=change_popup_status, img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
        BGM_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(res_buttons_pos_x[0]+text_width_BGM+GAME_BUTTON_INLINE_SPACING, res_buttons_pos_y[0]+0.3*HEIGHT),
                                    size=(res_buttons_size_x, res_buttons_size_y), text=BGM_altering_text,
                                    operation=play_BGM, img_mode=True, img_disabled=button_rect_darken,
                                img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken)
        increase_volume_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(res_buttons_pos_x[0]+text_width_BGM+2*GAME_BUTTON_INLINE_SPACING+res_buttons_size_x, res_buttons_pos_y[0]+0.3*HEIGHT),
                                    size=(small_bsize, res_buttons_size_y), text="+",
                                    operation=increase_volume, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
        decrease_volume_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(res_buttons_pos_x[0]+text_width_BGM+3*GAME_BUTTON_INLINE_SPACING+res_buttons_size_x+small_bsize, res_buttons_pos_y[0]+0.3*HEIGHT),
                                    size=(small_bsize, res_buttons_size_y), text="-",
                                    operation=decrease_volume, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
        all_button.append(popup_status_button)
        all_button.append(BGM_button)
        all_button.append(increase_volume_button)
        all_button.append(decrease_volume_button)
    menu_status = new_status
    pygame.time.wait(100) # This function was there to prevent mouse double clicking button / it does not work

def keep_the_game_running(things_to_draw=[]):
    """
        This function keep pygame updating and stop it from not responding
        you can also pass something to be drawn in draw_everything function here
    """
    # print(f"menu status {menu_status}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    WIN.fill(WHITE)
    if menu_status == 2:
        WIN.fill((88,179,184))
    # draw_everything(menu_status, things_to_draw)
    all_asset_count = 0

    for anime in all_animation:
        if anime.get_ident() == "cloud":
            # print(f"pos: {anime.get_pos()}, pause: {anime.pause}")
            if random.randint(0, 8000) < 10:
                anime.play()
            if anime.get_pos()[0] + anime.get_size()[0] < 0:
                anime.pause_animation()
                anime.set_pos((WIDTH, anime.get_pos()[1]))
        if anime.get_finish():
            all_animation.remove(anime)
            continue
        anime.draw_animation()
        all_asset_count += 1

    # game_button_control()
    for button in all_button:
        button.update_button()
        all_asset_count += 1

    # print(len(all_button))

    # game_popup_control()
    for popup in all_popup:
        if popup.get_finish():
            all_popup.remove(popup)
            continue
        if popup_enable:
            popup.draw()
        all_asset_count += 1

    # print(all_animation)
    draw_everything(menu_status, things_to_draw)

    for tl in top_level: # top level is for the upper most layer only
        all_asset_count += 1
        if type(tl) == Animation:
            if tl.get_finish():
                top_level.remove(tl)
                continue
            tl.draw_animation()
        elif type(tl) == Button:
            tl.update_button()
        elif type(tl) == Popup:
            if tl.get_finish():
                top_level.remove(tl)
                continue
            if popup_enable:
                tl.draw()
        
    # print(all_asset_count)
    # print("==========================")
    pygame.display.update()
    
def get_user_name(): # get input from user and store in user_name
    global user_name
    typing = True
    clock = pygame.time.Clock()
    while typing:
        clock.tick(FPS)
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
                    if len(user_name) >= 20:
                        all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render("Maximum name length is 20 characters", 1, BLACK)]))
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
    music_on = not music_on
    if not music_on:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    settings["music_on"] = music_on
    fo.save_settings(settings)
    change_game_status(5)

def increase_volume():
    global BGM_volume
    BGM_volume += 0.1
    if(BGM_volume > 1):
        BGM_volume = 1
    pygame.mixer.music.set_volume(BGM_volume)
    settings["volume"] = BGM_volume
    fo.save_settings(settings)
    all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render(f"Volume= {round(BGM_volume*10)}", 1, BLACK)]))
    
def decrease_volume():
    global BGM_volume
    BGM_volume -= 0.1
    if(BGM_volume < 0):
        BGM_volume = 0
    pygame.mixer.music.set_volume(BGM_volume)
    settings["volume"] = BGM_volume
    fo.save_settings(settings)
    all_popup.append(Popup(WIN, text_object=[DEFAULT_FONT.render(f"Volume= {round(BGM_volume*10)}", 1, BLACK)]))


def init_game():
    """this is the game"""
    global player_submit, game_input, all_button, user_name, background
    start_waiting_time = time.time()

    exit_and_gtfo_exist = False
    small_bsize, _ = calculate_button_position(1, border_factor=SMALL_BUTTON_BORDER_FACTOR, axis=WIDTH)
    _, y_border = calculate_button_position(1, edge_start=True, left_or_top_edge=True)
    _, one_bpos_x = calculate_button_position(2, size=small_bsize, edge_start=True,left_or_top_edge=False, axis=WIDTH)
    y_border = y_border[0]

    disc_message_1 = BIG_PIXEL_FONT.render("Disconnected", 1, BLACK)
    disc_message_2 = SMALL_PIXEL_FONT.render("Reason: Unable to establish connection to server", 1, BLACK)
    disc_message_3 = SMALL_PIXEL_FONT.render("Reason: Player disconnected", 1, BLACK)
    
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
        
        all_popup.append(Popup(WIN, text_object=[disc_message_1, disc_message_2]))
        # print(remove_animation_by_ident("space_background"))
        # print(remove_animation_by_ident("tile_colored"))
        # print(remove_animation_by_ident("tile_colored_cont"))
        change_game_status(new_status=2)
        return
    
    loop_status = 0
    current_array=[]
    current_sum=0


    while True:
        if menu_status != 3:
            net.client.close()
            return
        clock = pygame.time.Clock()
        clock.tick(FPS)
        waiting_time = math.ceil(time.time() - start_waiting_time)
        try:
            net.client.send(pickle.dumps(dummy))
            game = net.recv() # add try except here to prevent server crash
            if game is None:
                raise Exception
        except:
            all_popup.append(Popup(WIN, text_object=[disc_message_1, disc_message_3]))
            change_game_status(new_status=2)
            break

        if game.ready == False:
            waiting_time_rendered = DEFAULT_FONT.render(f"Waiting time: {waiting_time}", 1, WHITE)
            keep_the_game_running([(waiting_time_rendered, ((WIDTH - waiting_time_rendered.get_width()) / 2, (HEIGHT - waiting_time_rendered.get_height()) / 2))])
            #print("Waiting for another player")
            # keep_the_game_running()
            continue
        if game.p1_played and game.p2_played:
            game.update_score()
            try:
                net.client.send(pickle.dumps(game))
            except:
                all_popup.append(Popup(WIN, text_object=[disc_message_1, disc_message_3]))
                change_game_status(new_status=2)
                break
        if str(net.player) == str(game.turn):
            start_waiting_time = time.time()
            player_submit = False
            exit_and_gtfo_exist = False
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
            exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(one_bpos_x[0], y_border),size=(small_bsize, small_bsize), text="EXIT",
                                    operation=exit, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
            return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT, pos=(one_bpos_x[1], y_border),
                                    size= (small_bsize, small_bsize), text="back",
                                    operation=change_game_status, new_status=2, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
            all_button.append(return_to_mm1_button)
            all_button.append(exit_button)
            create_game_button(game.numbers_array)
            while not player_submit:
                clock.tick(FPS)
                if menu_status != 3:
                    net.client.close()
                    return
                if current_sum!=game.sum or current_array!=game.numbers_array:
                    current_array=game.numbers_array
                    current_sum=game.sum
                    all_button = []
                    
                    # print(small_bsize)
                    # print(one_bpos_x)
                    # print(y_border)
                    exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(one_bpos_x[0],y_border),size=(small_bsize, small_bsize), text="EXIT",
                                    operation=exit, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
                    return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT, pos=(one_bpos_x[1],y_border),
                                    size=(small_bsize, small_bsize), text="back",
                                    operation=change_game_status, new_status=2, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
                    all_button.append(return_to_mm1_button)
                    all_button.append(exit_button)
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
                    all_popup.append(Popup(WIN, text_object=[disc_message_1, disc_message_3]))
                    change_game_status(new_status=2)
                    break
                
                if str(net.player) != str(game.turn):
                    loop_status=1
                    break
                if math.ceil(60 - (time.time() - game.start_time)) < 0:
                    game_input = ""
                    break # I think break alone actually work
                sum_font = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), 200).render(f"{game.sum}", 1, WHITE)
                time_font = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), 120)
                # print(sum_font.get_size())

                time_text_color = WHITE
                if math.ceil(60 - (time.time() - game.start_time)) <= 10:
                    time_text_color = RED

                input_with_attitude = game_input if game_input != "" else "Please choose your input"
                to_draw_string = [DEFAULT_FONT.render(f"{game.p1_name}: {game.p1_score}", 1, WHITE),
                                DEFAULT_FONT.render(f"{game.p2_name}: {game.p2_score}", 1, WHITE),
                                DEFAULT_FONT.render(f"Time left: ", 1, WHITE),
                                time_font.render(f"{math.ceil(60 - (time.time() - game.start_time))}", 1, time_text_color),
                                DEFAULT_FONT.render(f"{input_with_attitude}", 1, WHITE),
                                sum_font                            
                                ]
                to_draw = [(to_draw_string[0], (HUD_BORDER_FACTOR*WIDTH, HUD_BORDER_FACTOR*HEIGHT)),
                           (to_draw_string[1], (HUD_BORDER_FACTOR*WIDTH, HUD_BORDER_FACTOR*HEIGHT+to_draw_string[1].get_height()+0.003*HEIGHT)),
                           (to_draw_string[2], (HUD_BORDER_FACTOR*WIDTH, HUD_BORDER_FACTOR*HEIGHT+2*to_draw_string[1].get_height()+2*0.003*HEIGHT)),
                           (to_draw_string[3], (HUD_BORDER_FACTOR*WIDTH, HUD_BORDER_FACTOR*HEIGHT+2.5*to_draw_string[1].get_height()+3*0.003*HEIGHT)),
                           (to_draw_string[4], (WIDTH // 2 - to_draw_string[4].get_width() // 2, int(0.3875 * HEIGHT) + (sum_font.get_height() // 8))),
                           (to_draw_string[5], (WIDTH//2-sum_font.get_width()//2, 0.25 * HEIGHT - sum_font.get_height() // 2))]
                keep_the_game_running(things_to_draw=to_draw)

            equation_str = game_input.replace("x", "*").replace("÷", "/")
            print(equation_str)
            if menu_status != 3:
                net.client.close()
                return
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
                start_waiting_time = time.time()
                
            except:
                all_popup.append(Popup(WIN, text_object=[disc_message_1, disc_message_3]))
                change_game_status(new_status=2)
                break
            print("send " + equation_str)
        else:
            # all_button = []
            # clock.tick(FPS)
            if not exit_and_gtfo_exist:
                exit_button = Button(window=WIN, button_font=DEFAULT_FONT,
                                    pos=(one_bpos_x[0], y_border),size=(small_bsize, small_bsize), text="EXIT",
                                    operation=exit, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
                return_to_mm1_button = Button(window=WIN, button_font=DEFAULT_FONT, pos=(one_bpos_x[1], y_border),
                                    size= (small_bsize, small_bsize), text="back",
                                    operation=change_game_status, new_status=2, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
                all_button.append(return_to_mm1_button)
                all_button.append(exit_button)
                exit_and_gtfo_exist = True
            waiting_time = math.ceil(time.time() - start_waiting_time)
            waiting_time_rendered = DEFAULT_FONT.render(f"Waiting time: {waiting_time}", 1, WHITE)
            keep_the_game_running([(waiting_time_rendered, ((WIDTH - waiting_time_rendered.get_width()) / 2, (HEIGHT - waiting_time_rendered.get_height()) / 2))])
    game_state = []

def user_game_input(button_input, button_index):
    """This the function that is called when user press the button in game session (numbers and operator)"""
    global game_input, disabled_game_button_index
    if button_input in ALL_ALLOWS_MATH_OP:
        print(f"{button_input}: operation")
    else:
        if game_input[len(game_input)-1:].isdigit(): # if last char is number, prevent them to input number
            print("pls choose op")
            text_1 = BIG_PIXEL_FONT.render("Warning", 1, BLACK)
            text_2 = DEFAULT_FONT.render(f"Please choose operation: {ALL_ALLOWS_MATH_OP}", 1, BLACK)
            all_popup.append(Popup(WIN, text_object=[text_1, text_2]))
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
    sum_font = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), 200)
    button = Button(WIN, sum_font, text=str(sum), operation=None, pos=(WIDTH/2, 150), size=(0, 0),
                    disabled_color=(255, 255, 255), text_color=WHITE)
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
    button_size_y, position_y = calculate_button_position(3, axis=HEIGHT, offset=0.2 * HEIGHT, border_factor=0.35) # Hard code : 3 is number of rows
    button_size_x, position_x = calculate_button_position(len(numbers), axis=WIDTH)
    current_number_of_button = len(all_button)
    for i in range(len(numbers)):
        button = Button(WIN, DEFAULT_FONT, text=str(numbers[i]), operation=user_game_input,
                        pos=(position_x[i], position_y[0]), size=(button_size_x, button_size_y),
                        button_input=str(numbers[i]), button_index=i+current_number_of_button, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(len(ALL_ALLOWS_MATH_OP), axis=WIDTH)

    for i in range(len(ALL_ALLOWS_MATH_OP)):
        button = Button(WIN, DEFAULT_FONT, text=ALL_ALLOWS_MATH_OP[i], operation=user_game_input,
                        pos=(position_x[i], position_y[1]), size=(button_size_x, button_size_y),
                        button_input=ALL_ALLOWS_MATH_OP[i], button_index=i, img_mode=True, img_disabled=button_square_bw,
                                    img_enabled=button_square, img_hover=button_square_brighten, img_pressed=button_square_darken)
        all_button.append(button)

    button_size_x, position_x = calculate_button_position(2, axis=WIDTH)
    reset_button = Button(WIN, DEFAULT_FONT, text="Reset", operation=reset_button_operation,
                          pos=(position_x[0], position_y[2]), size=(button_size_x, button_size_y), img_mode=True, img_disabled=button_rect_bw,
                                    img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken,)
    submit_button = Button(WIN, DEFAULT_FONT, text="Submit", operation=submit_button_operation,
                           pos=(position_x[1], position_y[2]), size=(button_size_x, button_size_y), img_mode=True, img_disabled=button_rect_bw,
                                    img_enabled=button_rect, img_hover=button_rect_brighten, img_pressed=button_rect_darken,)
    all_button.append(reset_button)
    all_button.append(submit_button)

def set_resolution(new_res):
    global WIDTH, HEIGHT, game_full_screen, settings, fo, font_size, SMALL_PIXEL_FONT, DEFAULT_FONT, BIG_PIXEL_FONT
    temp_res = WIN.get_size()
    old_res = WIN.get_size()
    
    if new_res == "0" or new_res == "1" or new_res == '2' or new_res == "3":
        new_res = int(new_res)
        temp_res = RESOLUTION_LIST[new_res][0], RESOLUTION_LIST[new_res][1]
        ratio_font_size = temp_res[0]/old_res[0]
        for i in range(len(font_size)):
            font_size[i] = int(font_size[i] * ratio_font_size)
        SMALL_PIXEL_FONT = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), font_size[0])
        DEFAULT_FONT = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), font_size[1])
        BIG_PIXEL_FONT = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), font_size[2])
    
    elif new_res == "full":
        game_full_screen = True
        settings["game_full_screen"] = True
    elif new_res == "unfull":
        game_full_screen = False
        settings["game_full_screen"] = False

    if temp_res[0] > SCREEN_SIZE[0] or temp_res[1] > SCREEN_SIZE[1]:
        all_popup.append(Popup(WIN, text_object=[BIG_PIXEL_FONT.render("WARNING", 1, BLACK),
                        SMALL_PIXEL_FONT.render(f"Your resolution is incompatible", 1, BLACK)]))
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
    font_size = [int(i * (WIDTH/OPTIMUM_RES[0])) for i in font_size]
    SMALL_PIXEL_FONT = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), font_size[0])
    DEFAULT_FONT = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), font_size[1])
    BIG_PIXEL_FONT = pygame.font.Font(os.path.join('Fonts', 'pixel_font.ttf'), font_size[2])
    BGM_volume = settings["volume"]
    pygame.mixer.music.set_volume(BGM_volume)
    if not music_on:
        pygame.mixer.music.pause()
    if game_full_screen:
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((WIDTH, HEIGHT))
    main()

print(all_button)