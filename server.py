import socket
from _thread import *
import pickle
from time import time
from game import Game

hostname=socket.gethostname()   
server=socket.gethostbyname(hostname)
port = 5555

def threaded_client(conn, player, gameId, games):
    global idCount
    conn.send(str.encode(str(player)))
    if gameId in games:
        game = games[gameId]
    # conn.sendall(pickle.dumps(game))
    reply = ""
    while True:
        rcv_game = pickle.loads(conn.recv(2048*5))
        # print("received")
        if gameId in games:
            game = games[gameId] 
            # Because this can have multiple games in the same time, so we need "gameId" to specify the game.
            if not rcv_game:
                break
            elif not rcv_game.dummy:
                games.pop(gameId)
                games[gameId] = rcv_game
                print(rcv_game.turn)
                print(games[gameId].turn)
            else:
                conn.sendall(pickle.dumps(game))
        else:
            break
        # except Exception as e:
            # print(e)
            # break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
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
            games[gameId] = Game(gameId, "MS Team", "Taiwan")
            print("Creating a new game...")
        else:
            games[gameId].ready = True
            games[gameId].startTime = time()
            player = 2

        print(games)
        start_new_thread(threaded_client, (conn, player, gameId, games))