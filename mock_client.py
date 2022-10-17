import pygame
import threading
from mock_network import Network
from utils import *

clientNumber = 0

def main():
    net = Network()
    game = net.recv()
    print("you are p"+str(net.player))
    while True:
        if net.player == game.turn:
            print("your turn")
            print(game.numbers_array)
            print(game.numbers_array)
            print(game.p1.score)
            print(game.p2.score)
            equation_str=input("")
            if net.player == 1:
                game.p1_played=True
                game.p1_cleared=game.check(equation_str)
            else:
                game.p2_played=True
                game.p2_cleared=game.check(equation_str)
            net.send(game)
        else:
            print("waiting for your turn")
            game=net.recv()
if __name__ == "__main__":
    main()