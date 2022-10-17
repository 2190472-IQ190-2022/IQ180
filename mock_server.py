import socket
from _thread import *
import pickle
from time import time
from game import Game

server = "10.202.133.244"
port = 5555

def threaded_client(conn, player, gameId, games):
    global idCount
    conn.send(str.encode(str(player)))
    if gameId in games:
        game = games[gameId]
    conn.sendall(pickle.dumps(game))
    reply = ""
    while True:
        try:
            data = pickle.load(conn.recv(2048*5))
            print("recieved")
            if gameId in games:
                game = games[gameId] 
                # Because this can have multiple games in the same time, so we need "gameId" to specify the game.

                if not data:
                    break
                elif type(data) == str:    
                    # if data == "reset":
                    #     game.resetWent()
                    if data == "get_equation":
                        game.generate_question()
                    elif data != "get":
                        game.check(player, data)
                conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

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
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")

    games = {}
    idCount = 0
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

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


        start_new_thread(threaded_client, (conn, player, gameId, games))