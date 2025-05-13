import random

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.bank = 0
        self.is_active = True

class PushYourLuckGame:
    def __init__(self):
        self.main_spinner = [1, 2, 3, 4, 5, 6, 7]
        self.players = []
        self.target_num = 0
        self.round_spinner = []
        self.game_over = False

    def add_player(self, name):
        self.players.append(Player(name))

    def start_new_round(self):
        # Reset round state
        self.round_spinner = self.main_spinner.copy()
        self.target_num = random.choice(self.round_spinner)
        self.round_spinner.remove(self.target_num)
        
        # Reset player states for new round
        for player in self.players:
            player.is_active = True
            player.bank = self.target_num

    def play_round(self):
        self.start_new_round()
        print(f"\nNew round starting! Target number is: {self.target_num}")
        
        if len(self.main_spinner) < 1:
            print(f"Congradulations, you won all the points!")
            return

        while any(p.is_active for p in self.players):
            # Get guesses from all active players
            guesses = {}
            for player in self.players:
                if player.is_active:
                    print(f"\n{player.name}'s turn!")
                    print(f"Spinner: {self.round_spinner}")
                    print(f"Target number: {self.target_num}")
                    print(f"Current bank: {player.bank}")
                    print(f"Current score: {player.score}")
                    
                    while True:
                        guess = input("Enter your guess (higher/lower/bank): ").lower()
                        if guess in ['higher', 'lower', 'bank']:
                            guesses[player] = guess
                            break
                        print("Invalid guess! Please enter 'higher', 'lower', or 'bank'")

            # Process all guesses
            next_num = random.choice(self.round_spinner)
            print(f"\nNext number is: {next_num}")
            
            for player, guess in guesses.items():
                if guess == 'bank':
                    player.score += player.bank
                    player.is_active = False
                    print(f"{player.name} banks {player.bank} points!")
                elif (guess == 'higher' and next_num > self.target_num) or \
                     (guess == 'lower' and next_num < self.target_num):
                    player.bank += next_num
                    print(f"{player.name} is correct! Bank is now {player.bank}")
                else:
                    print(f"{player.name} busts! Loses bank of {player.bank}")
                    player.is_active = False

            # Update target number and remove it from spinner
            self.target_num = next_num
            self.round_spinner.remove(next_num)

            # Check for winner
            for player in self.players:
                if player.score >= 100:
                    self.game_over = True
                    print(f"\n{player.name} wins with {player.score} points!")
                    return

def main():
    game = PushYourLuckGame()
    
    # Add players
    num_players = int(input("Enter number of players (2-4): "))
    while num_players < 2 or num_players > 4:
        num_players = int(input("Please enter a number between 2 and 4: "))
    
    for i in range(num_players):
        name = input(f"Enter name for player {i+1}: ")
        game.add_player(name)

    print("\nWelcome to Simultaneous Push Your Luck!")
    print("All players will guess for each target number.")
    print("First to reach 100 points wins!")

    # Main game loop
    while not game.game_over:
        game.play_round()
        
        if not game.game_over:
            print("\nRound summary:")
            for player in game.players:
                print(f"{player.name}: {player.score} points")

if __name__ == "__main__":
    main() 