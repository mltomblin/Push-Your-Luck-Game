import random
from push_your_luck_solver import PushYourLuckSolver
from typing import List, Dict, Optional, Tuple

class Player:
    def __init__(self, name: str, is_human: bool = False):
        self.name = name
        self.score = 0
        self.bank = 0
        self.is_active = True
        self.is_human = is_human

class SafePlayer(Player):
    """A player that always chooses to bank."""
    def get_guess(self, target_num: int, available_numbers: List[int]) -> str:
        return 'bank'

class ProbabilityPlayer(Player):
    """A player that makes decisions based on probability calculations."""
    def get_guess(self, target_num: int, available_numbers: List[int]) -> str:
        higher_count = sum(1 for num in available_numbers if num > target_num)
        lower_count = sum(1 for num in available_numbers if num < target_num)
        total = len(available_numbers)
        
        higher_prob = higher_count / total
        lower_prob = lower_count / total
        
        # If either option has >50% probability, choose that
        if higher_prob > 0.5:
            return 'higher'
        elif lower_prob > 0.5:
            return 'lower'
        else:
            return 'bank'

class ExpectedValuePlayer(Player):
    """A player that makes decisions based on expected payoffs."""
    def __init__(self, name: str, bank_threshold: float = 0.8, payoff_threshold: float = 0.1):
        super().__init__(name)
        self.bank_threshold = bank_threshold  # Bank if expected payoffs are below this fraction of current bank
        self.payoff_threshold = payoff_threshold  # Bank if payoffs are within this fraction of each other
    
    def calculate_expected_payoff(self, target_num: int, available_numbers: List[int], is_higher: bool) -> float:
        """Calculate expected payoff for higher or lower guess."""
        if is_higher:
            valid_numbers = [num for num in available_numbers if num > target_num]
            # If target is largest, this is an impossible guess
            if not valid_numbers:
                return float('-inf')  # Use negative infinity to ensure this option is never chosen
        else:
            valid_numbers = [num for num in available_numbers if num < target_num]
            # If target is smallest, this is an impossible guess
            if not valid_numbers:
                return float('-inf')  # Use negative infinity to ensure this option is never chosen
        
        # Expected payoff is the average of all valid numbers
        return sum(valid_numbers) / len(valid_numbers)
    
    def get_guess(self, target_num: int, available_numbers: List[int]) -> str:
        # Calculate expected payoffs
        higher_payoff = self.calculate_expected_payoff(target_num, available_numbers, True)
        lower_payoff = self.calculate_expected_payoff(target_num, available_numbers, False)
        
        # If both options are impossible (target is largest or smallest), bank
        if higher_payoff == float('-inf') and lower_payoff == float('-inf'):
            return 'bank'
        
        # Calculate probabilities
        higher_count = sum(1 for num in available_numbers if num > target_num)
        lower_count = sum(1 for num in available_numbers if num < target_num)
        total = len(available_numbers)
        
        higher_prob = higher_count / total
        lower_prob = lower_count / total
        
        # Calculate weighted expected payoffs (probability * payoff)
        # If payoff is -inf, the weighted payoff will also be -inf
        weighted_higher = higher_prob * higher_payoff if higher_payoff != float('-inf') else float('-inf')
        weighted_lower = lower_prob * lower_payoff if lower_payoff != float('-inf') else float('-inf')
        
        # Bank if:
        # 1. Both expected payoffs are low relative to current bank
        if weighted_higher != float('-inf') and weighted_lower != float('-inf') and \
           weighted_higher < self.bank * self.bank_threshold and \
           weighted_lower < self.bank * self.bank_threshold:
            return 'bank'
        
        # 2. Expected payoffs are very close to each other (and both are possible)
        if weighted_higher != float('-inf') and weighted_lower != float('-inf') and \
           abs(weighted_higher - weighted_lower) / max(weighted_higher, weighted_lower) < self.payoff_threshold:
            return 'bank'
        
        # 3. Current bank is already high relative to expected payoffs
        if weighted_higher != float('-inf') and weighted_lower != float('-inf') and \
           self.bank > max(weighted_higher, weighted_lower) * 1.5:
            return 'bank'
        
        # If one option is impossible, choose the other if it's possible
        if weighted_higher == float('-inf'):
            return 'lower' if weighted_lower != float('-inf') else 'bank'
        if weighted_lower == float('-inf'):
            return 'higher' if weighted_higher != float('-inf') else 'bank'
        
        # Otherwise, choose the option with higher weighted expected payoff
        return 'higher' if weighted_higher > weighted_lower else 'lower'

class AIPlayer(Player):
    """A player that uses the trained Q-learning solver."""
    def __init__(self, name: str):
        super().__init__(name)
        self.solver = PushYourLuckSolver()
        self.solver.load_model()  # Load the trained model
        self.solver.exploration_rate = 0  # Disable exploration for actual play
    
    def get_guess(self, target_num: int, available_numbers: List[int]) -> str:
        state_key = self.solver.get_state_key(self.score, self.bank, target_num, available_numbers)
        return self.solver.get_action(state_key)

class MixedPushYourLuckGame:
    def __init__(self):
        self.main_spinner = list(range(1, 14))  # [1, 2, ..., 13]
        self.players: List[Player] = []
        self.target_num = 0
        self.round_spinner = []
        self.game_over = False
        self.target_score = 100  # Using 100 as target score for multiplayer
    
    def add_player(self, player: Player):
        """Add a player to the game."""
        self.players.append(player)
    
    def start_new_round(self):
        """Reset round state and player states."""
        self.round_spinner = self.main_spinner.copy()
        self.target_num = random.choice(self.round_spinner)
        self.round_spinner.remove(self.target_num)
        
        # Reset player states for new round
        for player in self.players:
            player.is_active = True
            player.bank = self.target_num
    
    def get_human_guess(self, player: Player) -> str:
        """Get guess from human player."""
        while True:
            print(f"\n{player.name}'s turn!")
            print(f"Spinner: {self.round_spinner}")
            print(f"Target number: {self.target_num}")
            print(f"Current bank: {player.bank}")
            print(f"Current score: {player.score}")
            
            guess = input("Enter your guess (higher/lower/bank): ").lower()
            if guess in ['higher', 'lower', 'bank']:
                return guess
            print("Invalid guess! Please enter 'higher', 'lower', or 'bank'")
    
    def play_round(self):
        """Play a single round of the game."""
        self.start_new_round()
        print(f"\nNew round starting! Target number is: {self.target_num}")
        
        while any(p.is_active for p in self.players):
            # Get guesses from all active players
            guesses: Dict[Player, str] = {}
            
            for player in self.players:
                if player.is_active:
                    if player.is_human:
                        guess = self.get_human_guess(player)
                    else:
                        guess = player.get_guess(self.target_num, self.round_spinner)
                        print(f"{player.name}'s turn (Score: {player.score}) - Chooses: {guess}")
                    
                    guesses[player] = guess
            
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
                if player.score >= self.target_score:
                    self.game_over = True
                    print(f"\n{player.name} wins with {player.score} points!")
                    print("\nFinal Scores:")
                    for p in sorted(self.players, key=lambda x: x.score, reverse=True):
                        print(f"{p.name}: {p.score} points")
                    return

def main():
    game = MixedPushYourLuckGame()
    
    # Add players
    human_name = input("Enter your name: ")
    human_player = Player(human_name, is_human=True)
    game.add_player(human_player)
    
    # Add AI players
    game.add_player(AIPlayer("AI Solver"))
    game.add_player(SafePlayer("Safe Player"))
    game.add_player(ProbabilityPlayer("Probability Player"))
    game.add_player(ExpectedValuePlayer("Expected Value Player"))
    
    print("\nWelcome to Mixed Push Your Luck!")
    print("You will be playing against:")
    print("1. AI Solver (uses Q-learning)")
    print("2. Safe Player (always banks)")
    print("3. Probability Player (uses probability calculations)")
    print("4. Expected Value Player (uses expected payoff calculations)")
    print("\nFirst to reach 100 points wins!")

    # Main game loop
    while not game.game_over:
        game.play_round()
        
        if not game.game_over:
            print("\nRound summary:")
            for player in game.players:
                print(f"{player.name}: {player.score} points")

if __name__ == "__main__":
    main() 