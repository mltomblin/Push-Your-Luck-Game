import numpy as np
import random
from collections import defaultdict
import pickle
from typing import List, Tuple, Dict
import time

class PushYourLuckSolver:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, min_exploration_rate=0.01, exploration_decay=0.995):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.min_exploration_rate = min_exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.main_spinner = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # Using the same spinner as the game
        #self.main_spinner = [1, 2, 3, 4, 5]  # smaller spinner for testing
        self.target_score = 100
        
    def get_state_key(self, score: int, bank: int, target_num: int, available_numbers: List[int]) -> str:
        """Convert the game state into a string key for the Q-table."""
        return f"{score}_{bank}_{target_num}_{','.join(map(str, sorted(available_numbers)))}"
    
    def get_action(self, state: str) -> str:
        """Choose an action using epsilon-greedy strategy."""
        if random.random() < self.exploration_rate:
            return random.choice(['higher', 'lower', 'bank'])
        else:
            actions = self.q_table[state]
            if not actions:
                return random.choice(['higher', 'lower', 'bank'])
            return max(actions.items(), key=lambda x: x[1])[0]
    
    def update_q_value(self, state: str, action: str, reward: float, next_state: str):
        """Update Q-value using the Q-learning formula."""
        current_q = self.q_table[state][action]
        next_max_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state][action] = new_q
    
    def train(self, num_episodes: int = 10000):
        """Train the solver by playing multiple games."""
        wins = 0
        total_rounds = 0
        
        for episode in range(num_episodes):
            score = 0
            rounds_played = 0
            game_over = False
            
            while not game_over:
                # Start new round
                round_spinner = self.main_spinner.copy()
                target_num = random.choice(round_spinner)
                round_spinner.remove(target_num)
                bank = target_num
                rounds_played += 1
                
                while True:
                    # Get current state
                    current_state = self.get_state_key(score, bank, target_num, round_spinner)
                    
                    # Choose action
                    action = self.get_action(current_state)
                    
                    # Take action
                    if action == 'bank':
                        score += bank
                        reward = -1  # Penalty for each round
                        next_state = self.get_state_key(score, 0, 0, [])  # Game will start new round
                        self.update_q_value(current_state, action, reward, next_state)
                        break
                    
                    if len(round_spinner) < 2:
                        score += bank
                        reward = -1  # Round penalty
                        next_state = self.get_state_key(score, 0, 0, [])
                        self.update_q_value(current_state, 'bank', reward, next_state)
                        break
                    
                    next_num = random.choice(round_spinner)
                    round_spinner.remove(next_num)
                    
                    if (action == 'higher' and next_num > target_num) or \
                       (action == 'lower' and next_num < target_num):
                        bank += next_num
                        target_num = next_num
                        reward = 3  # Reward for correct guess
                        next_state = self.get_state_key(score, bank, target_num, round_spinner)
                    else:
                        reward = -2  # Bust penalty
                        next_state = self.get_state_key(score, 0, 0, [])
                    
                    # Add round penalty to all non-banking actions
                    if action != 'bank':
                        reward -= 1  # Round penalty
                    
                    self.update_q_value(current_state, action, reward, next_state)
                    
                    if reward == -3:  # Bust (-2) + Round penalty (-1)
                        break
                
                if score >= self.target_score:
                    game_over = True
                    wins += 1
                    reward = 100  # Big reward for winning
                    self.update_q_value(current_state, action, reward, next_state)
            
            total_rounds += rounds_played
            
            # Decay exploration rate
            self.exploration_rate = max(self.min_exploration_rate, 
                                     self.exploration_rate * self.exploration_decay)
            
            if (episode + 1) % 100 == 0:
                win_rate = wins / (episode + 1) * 100
                avg_rounds = total_rounds / (episode + 1)
                print(f"Episode {episode + 1}/{num_episodes}")
                print(f"Win rate: {win_rate:.2f}%")
                print(f"Average rounds per game: {avg_rounds:.2f}")
                print(f"Exploration rate: {self.exploration_rate:.3f}")
                print("---")
    
    def save_model(self, filename: str = "push_your_luck_model.pkl"):
        """Save the trained Q-table to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
    
    def load_model(self, filename: str = "push_your_luck_model.pkl"):
        """Load a trained Q-table from a file."""
        try:
            with open(filename, 'rb') as f:
                self.q_table = defaultdict(lambda: defaultdict(float), pickle.load(f))
            print("Model loaded successfully!")
        except FileNotFoundError:
            print("No saved model found.")
    
    def play_game(self, verbose: bool = True) -> Tuple[int, int]:
        """Play a single game using the learned strategy."""
        score = 0
        rounds_played = 0
        game_over = False
        
        while not game_over:
            # Start new round
            round_spinner = self.main_spinner.copy()
            target_num = random.choice(round_spinner)
            round_spinner.remove(target_num)
            bank = target_num
            rounds_played += 1
            
            if verbose:
                print(f"\nRound {rounds_played}")
                print(f"Score: {score}")
                print(f"Target number: {target_num}")
                print(f"Available numbers: {round_spinner}")
            
            while True:
                current_state = self.get_state_key(score, bank, target_num, round_spinner)
                action = self.get_action(current_state)
                
                if verbose:
                    print(f"\nCurrent bank: {bank}")
                    print(f"Action chosen: {action}")
                
                if action == 'bank':
                    score += bank
                    if verbose:
                        print(f"Banked {bank} points! New score: {score}")
                    break
                
                if len(round_spinner) < 2:
                    score += bank
                    if verbose:
                        print(f"Last number! Banked {bank} points! New score: {score}")
                    break
                
                next_num = random.choice(round_spinner)
                round_spinner.remove(next_num)
                
                if verbose:
                    print(f"Next number: {next_num}")
                
                if (action == 'higher' and next_num > target_num) or \
                   (action == 'lower' and next_num < target_num):
                    bank += next_num
                    target_num = next_num
                    if verbose:
                        print(f"Correct! Bank increased to {bank}")
                else:
                    if verbose:
                        print(f"Bust! Lost bank of {bank}")
                    break
            
            if score >= self.target_score:
                game_over = True
                if verbose:
                    print(f"\nGame won in {rounds_played} rounds!")
                    print(f"Final score: {score}")
        
        return score, rounds_played

def main():
    solver = PushYourLuckSolver()
    
    # Try to load existing model
    solver.load_model()
    
    # Train the solver
    print("Training the solver...")
    start_time = time.time()
    solver.train(num_episodes=10000)
    training_time = time.time() - start_time
    print(f"\nTraining completed in {training_time:.2f} seconds")
    
    # Save the trained model
    solver.save_model()
    
    # Play some games using the learned strategy
    print("\nPlaying games with learned strategy:")
    num_games = 5
    total_rounds = 0
    wins = 0
    
    for i in range(num_games):
        print(f"\nGame {i+1}/{num_games}")
        score, rounds = solver.play_game(verbose=True)
        total_rounds += rounds
        if score >= 50:
            wins += 1
    
    print(f"\nResults over {num_games} games:")
    print(f"Win rate: {wins/num_games*100:.2f}%")
    print(f"Average rounds per game: {total_rounds/num_games:.2f}")

if __name__ == "__main__":
    main() 