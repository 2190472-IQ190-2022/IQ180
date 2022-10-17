import socket
from _thread import *
import pickle
from game import Game

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

try:              #in case port is full
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #listen 2 client
print("Waiting for a connection, Server Started")

connected = set() #store ip addr
games = {} #store our gameId tell which game is run using gameId
idCount = 0 #count game that run

def threaded_client(conn, player, gameId):  # for run many process simontanously
    global idCount # keep track how many people, game
    conn.send(str.encode(str(player))) # tell whether who u r

    reply = ""
    while True: #important send 1 of 3 options Get(get game from server), Reset(reset game in both player),Move( in play part)
        try:
            data = conn.recv(4096).decode() #data that send

            if gameId in games: #check if gameId still in [] games
                game = games[gameId] # so this is game V play

                if not data: # check whether 1 0f 3 options
                    break
                else:
                    if data == "reset": #check if got reset
                        game.reset()
                    elif data != "get": # not reset and get so it's move
                        game.game_started(player, data) #use start game

                    conn.sendall(pickle.dumps(game)) #send to all client what in screen
            else:# 
                break
        except:
            break

    print("Lost connection") # close game& Delete it
    try:
        del games[gameId] #delete game
        print("Closing Game", gameId) #close game
    except:
        pass
    idCount -= 1
    conn.close()

    


    while True: # check amount player
        conn, addr = s.accept()
        print("Connected to:", addr)

        idCount +=1 #keep track how many player connect
        player = 0 # current player 0 or 1
        gameId = (idCount -1)//2 #how many game per pair
        if idCount % 2 == 1: #check whether there is  player
            games[gameId] = Game(gameId) # create new game
            print("Creating a new game... ")
        else:
            games[gameId].ready = True 
            player = 1
            
        
        start_new_thread(threaded_client, (conn, player, gameId))