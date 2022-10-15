from time import time
class Game:
    def __init__(self, id, p1_name, p2_name):
        self.p1_score = 0
        self.p2_score = 0
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.turn = 0 # 1 for player 1's turn and 2 for player 2's turn
        self.id = id
        self.start_time = 0
        self.game_time_p1 = 0
        self.game_time_p2 = 0
        self.p1_cleared = False
        self.p2_cleared = False
        self.p1_played = False
        self.p2_played = False
    def generate_question():
        #generate each digits and answer
        pass
    def check():
        pass
    def reset():
        pass
    def update_score():
        #Define the winner of current round by comparing boolean cleared and game_time, then update score and player's turn
        pass
    def game_started():
        #Set player
        pass
