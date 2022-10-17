# import pygame
import time
import threading
import pickle
from mock_network import Network

clientNumber = 0


def main():
    net = Network()
    # game = net.recv()
    print("you are p"+str(net.player))
    while True:
        game = net.recv()
        print(game.turn)
        if game.p1_played and game.p2_played:
            game.update_score()
        if str(net.player) == str(game.turn):
            print("your turn")
            print(game.numbers_array)
            print(game.sum)
            print(game.p1_score)
            print(game.p2_score)
            equation_str = input("")
            if net.player == 1:
                game.p1_played = True
                game.p1_cleared = game.check(equation_str)
            else:
                game.p2_played = True
                game.p2_cleared = game.check(equation_str)
            net.client.send(pickle.dumps(game))
            print("send")
        else:
            print("waiting for your turn")
        time.sleep(1)


if __name__ == "__main__":
    main()
