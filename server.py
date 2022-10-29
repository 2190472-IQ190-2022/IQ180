import math
import socket
from _thread import *
import pickle
from time import time
from game import Game
import pygame
from Button import Button
from Popup import Popup

hostname=socket.gethostname()
server=socket.gethostbyname(hostname)
# server = "10.201.142.11"
port = 5555
resetID = 0

# UI part
user_input = ""
width, height = 800, 600
button_size = 100
# end of UI Part

def reset_game(game_ID):
    if game_ID == "":
        reset_games() # ไอสัสมึงลืม s ไปตัวนึงกูนั่ง debug อยู่ตั้งนาน
        print("reset all game")
    else:
        try:
            games[game_ID].reset()
            print(f"reset game #{game_ID}")
        except:
            print("Error, most likely index out of bound")
def reset_games():
    for e in games:
        reset_game(e)

def test_func(name):
    print(f"hello {name}")
    
def threaded_client(conn, player, gameId, games):
    global idCount
    conn.send(str.encode(str(player)))
    if gameId in games:
        game = games[gameId]
    # conn.sendall(pickle.dumps(game))
    reply = ""
    while True:
        try:
            rcv_game = pickle.loads(conn.recv(2048*5))
            # print("received")
            if gameId in games:
                game = games[gameId]
                # Because this can have multiple games in the same time, so we need "gameId" to specify the game.
                if not rcv_game:
                    break
                elif not rcv_game.dummy:
                    print("received")
                    if rcv_game.ready:
                        if rcv_game.turn == 2: # turn is already updated before sending to server
                            print("PASS 1")
                            rcv_game.p1_game_time = math.ceil(60 - (time() - rcv_game.startTime))
                            rcv_game.startTime = time()
                            # rcv_game.turn = 2
                        elif rcv_game.turn == 1: # turn is already updated before sending to server
                            print("PASS 2")
                            rcv_game.p2_game_time = math.ceil(60 - (time() - rcv_game.startTime))
                            rcv_game.startTime = time()
                            # rcv_game.turn = 1
                    games[gameId] = rcv_game
                    print(f"P1 spends {rcv_game.p1_game_time}")
                    print(f"P2 spends {rcv_game.p2_game_time}")
                    print("--------------------------------")
                    # print(rcv_game.turn)
                    # print(games[gameId].turn)
                else:
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    print(f"The number of players: {idCount}")
    conn.close()


def UI():
    global user_input
    WIN = pygame.display.set_mode((width, height))
    pygame.font.init()
    server_font = pygame.font.SysFont('comicsans', 40)
    
    running = True
    
    reset_all_button = Button(WIN, button_font=server_font, pos=(0.25*width-0.5*button_size, 0.5*height-0.5*button_size), 
                        text="reset all", enabled_color=(255, 0, 0), operation=reset_game, game_ID="")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        typing = True
        while typing:
            reset_button = Button(WIN, button_font=server_font, pos=(0.75*width-0.5*button_size, 0.5*height-0.5*button_size), 
                        text="reset", enabled_color=(255, 0, 0), operation=reset_game, game_ID=user_input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[0:-1]
                    elif event.key == pygame.K_RETURN:
                        typing = False
                        reset_game(user_input)
                    else:
                        user_input += event.unicode
                print_text = server_font.render(f"type game id: {user_input}", 1, (0, 0, 0))
                WIN.fill((255, 255, 255))
                pos_x, pos_y = width/2-(print_text.get_width()/2), height/4-(print_text.get_height()/2)
                WIN.blit(print_text, (pos_x, pos_y, 200, 200))
                reset_all_button.update_button()
                reset_button.update_button()
                pygame.display.update()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    s.listen(2)
    print("Waiting for a connection, Server Started")

    start_new_thread(UI, ())
    games = {}
    idCount = 0
    while True:
        conn, addr = s.accept()
        print("Connected to:", conn)

        idCount += 1
        player = 1
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId, "Player1", "Player2")
            games[gameId].dummy = False
            print("Creating a new game...")
        else:
            games[gameId].ready = True
            games[gameId].startTime = time()
            player = 2

        print(f"The number of players: {idCount}")
        start_new_thread(threaded_client, (conn, player, gameId, games))