from time import time
class Game:
    def __init__(self, id, p1_name, p2_name):
        self.p1_score = 0
        self.p2_score = 0
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.turn = 0 # 1 for player 1's turn and 2 for player 2's turn
        self.id = id
        #for timer
        self.start_time = 0
        #duration the player have spent to clear the question
        self.game_time_p1 = 0
        self.game_time_p2 = 0
        #Whether or not players have cleared the question
        self.p1_cleared = False
        self.p2_cleared = False
        #Whether or not players have played their turn
        self.p1_played = False
        self.p2_played = False
    def generate_question():
        #generate each digits and answer
        pass
    def check(string_equation, answer):
        #Check the answer of the equation
        return eval(string_equation)==answer
    def reset():
        #reset the game, scores and etc.
        pass
    def new_round():
        p1_cleared=False
        p2_cleared=False
        p1_played=False
        p2_played=False
        game_time_p1=0
        game_time_p2=0
    def update_score():
        #Define the winner of current round by comparing boolean cleared and game_time, then update score and player's turn
        if p1_cleared and p2_cleared:
            if game_time_p1 < game_time_p2:
                p1_score+=1
                turn=1
            else if game_time_p1 > game_time_p2:
                p2_score+=1
                turn=2
        else if p1_cleared:
            p1_score+=1
            turn=1
        else if p2_cleared:
            p2_score+=1
            turn=2
        new_round()
    def game_started():
        #Random first player in the first game (And maybe other purpose)
        pass
