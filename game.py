from time import time
import random

class Game:
    def __init__(self, id, p1_name, p2_name):
        self.p1_score = 0
        self.p2_score = 0
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.current_time = 0
        self.ready = False
        self.dummy = True
        self.turn = random.getrandbits(1)+1  # 1 for player 1's turn and 2 for player 2's turn
        self.id = id
        # for timer
        # Server initialize the start time by start_time = time.time()
        # to use in server, time.time()-start_time
        self.start_time = 0
        # duration the player have spent to clear the question
        self.p1_game_time = 0
        self.p2_game_time = 0
        # Whether or not players have cleared the question
        self.p1_cleared = False
        self.p2_cleared = False
        # Whether or not players have played their turn
        self.p1_played = False
        self.p2_played = False
        # number array and answer for the question
        self.numbers_array, self.equation, self.sum = self.generate_question()

    def set_name(self, player, name):
        #Spacebar is not allowed for the sake simplicity (In the process of checking empty username)
        name.replace(" ","")
        #Name "Player1" is not allowed for player 2, likewise "Player2" is not allowed for player 1
        if str(player) == '1' and name == "Player2":
            name=""
        elif str(player) == '2' and name == "Player1":
            name=""
        if len(name) == 0:
            name += "Player" + str(player)
        if str(player) == '1':
            self.p1_name = name
        elif str(player) == '2':
            self.p2_name = name
        #Handle duplicate name
        if self.p1_name == self.p2_name:
            self.p1_name+='(1)'
            self.p2_name+='(2)'

    def generate_question(self):
        # generate each digits and answer
        operation = ["+","-","*"] # add, minus, time(multiply)
        have_divide = random.getrandbits(1)
        numbers_array = []
        equation = ""
        sum = -1
        while True:
            equation = ""
            del numbers_array[:]
            number_of_digits = 4 if have_divide == 1 else 5
            sum = -1
            for i in range(number_of_digits):
                digit = random.randint(1, 9)
                numbers_array.append(digit)
                equation += str(digit)
                if i != number_of_digits-1:
                    equation += random.choice(operation)
            sum = eval(equation)
            if have_divide == 1:
                for i in range(9,0,-1):
                    if sum%i == 0:
                        sum /= i
                        sum = int(sum)
                        numbers_array.append(i)
                        equation = f"({equation})/{str(i)}"
                        break
            if sum >= 10:
                break


        # For Debugging Purpose. May remove when submitting to ajarn
        # print(equation)
        # print(eval(equation))
        # print(sum)
        # print(numbers_array)
        # End of Debugging section
        self.sum = sum
        random.shuffle(numbers_array)
        self.numbers_array=numbers_array
        return numbers_array, equation, sum

    def check(self, string_equation):
        # Check the answer of the equation
        numbers=0
        for e in string_equation:
            testCharacter=""+ e
            if testCharacter.isnumeric():
                numbers+=1
        if numbers!=5:
            return False
        try:
            return eval(string_equation) == self.sum
        except:
            return False

    def reset(self):
        # reset the game, scores and etc.
        self.p1_score = 0
        self.p2_score = 0
        self.turn = random.getrandbits(1)+1
        self.new_round()


    def new_round(self):
        self.p1_cleared = False
        self.p2_cleared = False
        self.p1_played = False
        self.p2_played = False
        self.p1_game_time = 0
        self.p2_game_time = 0
        self.numbers_array, self.equation,self.sum = self.generate_question()
        

    def update_score(self):
        # Define the winner of current round by comparing boolean cleared and game_time, then update score and player's turn
        if self.p1_cleared and self.p2_cleared:
            if self.p1_game_time > self.p2_game_time:
                self.p1_score += 1
                self.turn = 1
            elif self.p1_game_time < self.p2_game_time:
                self.p2_score += 1
                self.turn = 2
        elif self.p1_cleared:
            self.p1_score += 1
            self.turn = 1
        elif self.p2_cleared:
            self.p2_score += 1
            self.turn = 2
        self.new_round()

    def game_started(self):
        # Choose the first player.
        # The first game will random.
        # The following game will be set by the server according to the winner of the previous round.
        return self.turn
