import math
import socket
from _thread import *
import pickle
from time import time
from game import Game

hostname=socket.gethostname()
server=socket.gethostbyname(hostname)
# server = "10.201.142.11"
port = 5555
resetID = 0
def reset_game(game_ID):
    if game_ID == "":
        reset_game()
    else:
        try:
            games[game_ID].reset()
        except:
            print("Error, most likely index out of bound")
def reset_games():
    for e in games:
        reset_game(e)
    
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

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    s.listen(2)
    print("Waiting for a connection, Server Started")

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