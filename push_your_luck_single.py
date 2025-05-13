import random

class PushYourLuckGame:
    def __init__(self):
        #self.main_spinner = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.main_spinner = [1, 2, 3, 4, 5] #smaller list for testing
        self.score = 0
        self.bank = 0
        self.target_num = 0
        self.round_spinner = []
        self.game_over = False

    def start_new_round(self):
        # Reset round state
        self.round_spinner = self.main_spinner.copy()
        self.target_num = random.choice(self.round_spinner)
        #self.target_num = self.round_spinner[0] #test spinner
        self.round_spinner.remove(self.target_num)
        self.bank = self.target_num

    def play_round(self):
        
        self.start_new_round()

        if self.score >= 50:
            self.game_over = True
            print(f"\nYou win with {self.score} points!")
            return
       
        print(f"\nNew round starting! Target number is: {self.target_num}")
        
        while not self.game_over:
            print(f"\nYour turn!")
            print(f"Spinner: {self.round_spinner}")
            print(f"Target number: {self.target_num}")
            print(f"Current bank: {self.bank}")
            print(f"Your score: {self.score}")
            
            guess = input("Enter your guess (higher/lower/bank): ").lower()
            
            if len(self.round_spinner) < 2:
                self.score += self.bank
                print(f"Congratulations, you won the whole round and banked {self.bank} points!")
                return

            if guess == 'bank':
                self.score += self.bank
                print(f"\nYou banked {self.bank} points!")
                return
            
            if guess not in ['higher', 'lower']:
                print("Invalid guess! Please enter 'higher', 'lower', or 'bank'")
                continue

            next_num = random.choice(self.round_spinner)
            #next_num = self.round_spinner[0]
            print(f"\nNext number is: {next_num}")
            
            if (guess == 'higher' and next_num > self.target_num) or \
               (guess == 'lower' and next_num < self.target_num):
                self.bank += next_num
                self.target_num = next_num
                self.round_spinner.remove(next_num)
                print(f"Correct! Bank is now {self.bank}")
            else:
                print(f"Bust! You lose your bank of {self.bank}")
                return

def main():
    game = PushYourLuckGame()
    print("Welcome to Single Player Push Your Luck!")
    print("Try to reach 50 points by guessing if the next number will be higher or lower.")
    print("Bank your points when you want to play it safe!")
    
    while not game.game_over:
        game.play_round()
        

        #if not game.game_over:
            #print("\nRound summary:")
            #print(f"Your score: {game.score} points")

if __name__ == "__main__":
    main() 