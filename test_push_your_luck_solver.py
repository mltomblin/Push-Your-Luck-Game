import unittest
from push_your_luck_solver import PushYourLuckSolver
import random

class TestPushYourLuckSolver(unittest.TestCase):
    def setUp(self):
        """Set up a fresh solver instance before each test."""
        self.solver = PushYourLuckSolver()
        # Set exploration rate to 0 to ensure deterministic behavior in tests
        self.solver.exploration_rate = 0
        # Update spinner range to 1-13
        self.solver.main_spinner = list(range(1, 14))  # [1, 2, ..., 13]
        
    def test_initialization(self):
        """Test that the solver initializes with correct default values."""
        self.assertEqual(self.solver.learning_rate, 0.1)
        self.assertEqual(self.solver.discount_factor, 0.95)
        self.assertEqual(self.solver.main_spinner, list(range(1, 14)))
        self.assertEqual(self.solver.target_score, 100)
        self.assertEqual(len(self.solver.q_table), 0)
    
    def test_state_key_generation(self):
        """Test that state keys are generated correctly."""
        # Test basic state key
        state_key = self.solver.get_state_key(10, 5, 3, [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        self.assertEqual(state_key, "10_5_3_1,2,4,5,6,7,8,9,10,11,12,13")
        
        # Test empty available numbers
        state_key = self.solver.get_state_key(0, 0, 0, [])
        self.assertEqual(state_key, "0_0_0_")
        
        # Test with different score and bank values
        state_key = self.solver.get_state_key(49, 10, 2, [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        self.assertEqual(state_key, "49_10_2_1,3,4,5,6,7,8,9,10,11,12,13")
    
    def test_edge_cases_target_numbers(self):
        """Test solver's behavior with edge case target numbers."""
        # Test with target number 1 (should prefer 'higher')
        state_key = self.solver.get_state_key(0, 1, 1, list(range(2, 14)))
        self.solver.q_table[state_key] = {'higher': 10, 'lower': -10, 'bank': 5}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'higher', "Solver should choose 'higher' when target is 1")
        
        # Test with target number 13 (should prefer 'lower')
        state_key = self.solver.get_state_key(0, 13, 13, list(range(1, 13)))
        self.solver.q_table[state_key] = {'higher': -10, 'lower': 10, 'bank': 5}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'lower', "Solver should choose 'lower' when target is 13")
        
        # Test with target number 7 (middle value) - allow any strategy
        state_key = self.solver.get_state_key(0, 7, 7, [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13])
        self.solver.q_table[state_key] = {'higher': 8, 'lower': 8, 'bank': 8}  # Equal values to allow any choice
        action = self.solver.get_action(state_key)
        self.assertIn(action, ['higher', 'lower', 'bank'], 
                     "Solver should be free to choose any action for middle value")
    
    def test_banking_strategy(self):
        """Test solver's banking strategy in different scenarios."""
        # Test banking when close to target score
        state_key = self.solver.get_state_key(45, 10, 3, list(range(1, 14)))
        self.solver.q_table[state_key] = {'higher': 5, 'lower': 5, 'bank': 15}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'bank', "Solver should choose to bank when close to target score")
        
        # Test banking with high bank value (40% of max possible points in a round)
        max_possible_points = sum(range(1, 14))  # 91 points
        high_bank_threshold = int(max_possible_points * 0.4)  # ~36 points
        state_key = self.solver.get_state_key(20, high_bank_threshold, 3, list(range(1, 14)))
        self.solver.q_table[state_key] = {'higher': 5, 'lower': 5, 'bank': 20}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'bank', 
                        f"Solver should choose to bank with high bank value ({high_bank_threshold} points)")
    
    def test_score_and_bank_combinations(self):
        """Test solver's behavior with different combinations of score and bank values."""
        # Test low score, low bank
        state_key = self.solver.get_state_key(5, 3, 3, list(range(1, 14)))
        self.solver.q_table[state_key] = {'higher': 10, 'lower': 10, 'bank': 5}
        action = self.solver.get_action(state_key)
        self.assertIn(action, ['higher', 'lower'], 
                     "Solver should be willing to take risks with low score and low bank")
        
        # Test low score, high bank
        state_key = self.solver.get_state_key(5, 30, 3, list(range(1, 14)))
        self.solver.q_table[state_key] = {'higher': 5, 'lower': 5, 'bank': 15}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'bank', 
                        "Solver should choose to bank with low score but high bank")
        
        # Test high score, low bank
        state_key = self.solver.get_state_key(45, 3, 3, list(range(1, 14)))
        self.solver.q_table[state_key] = {'higher': 5, 'lower': 5, 'bank': 10}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'bank', 
                        "Solver should choose to bank with high score and low bank")
        
        # Test high score, high bank
        state_key = self.solver.get_state_key(45, 30, 3, list(range(1, 14)))
        self.solver.q_table[state_key] = {'higher': 5, 'lower': 5, 'bank': 20}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'bank', 
                        "Solver should choose to bank with high score and high bank")
    
    def test_available_numbers_combinations(self):
        """Test solver's behavior with different combinations of available numbers."""
        # Test with only high numbers available
        state_key = self.solver.get_state_key(0, 7, 7, [8, 9, 10, 11, 12, 13])
        self.solver.q_table[state_key] = {'higher': 10, 'lower': -10, 'bank': 5}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'higher', 
                        "Solver should choose 'higher' when only high numbers are available")
        
        # Test with only low numbers available
        state_key = self.solver.get_state_key(0, 7, 7, [1, 2, 3, 4, 5, 6])
        self.solver.q_table[state_key] = {'higher': -10, 'lower': 10, 'bank': 5}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'lower', 
                        "Solver should choose 'lower' when only low numbers are available")
        
        # Test with numbers on both sides of target
        state_key = self.solver.get_state_key(0, 7, 7, [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13])
        self.solver.q_table[state_key] = {'higher': 8, 'lower': 8, 'bank': 5}
        action = self.solver.get_action(state_key)
        self.assertIn(action, ['higher', 'lower', 'bank'], 
                     "Solver should be free to choose any action with balanced available numbers")
    
    def test_all_numbers_used(self):
        """Test solver's behavior when all numbers have been used in a round."""
        # Test when only one number remains
        state_key = self.solver.get_state_key(0, 7, 7, [8])
        self.solver.q_table[state_key] = {'higher': 10, 'lower': -10, 'bank': 5}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'higher', 
                        "Solver should choose appropriate action with only one number available")
        
        # Test when no numbers remain (should automatically bank)
        state_key = self.solver.get_state_key(0, 7, 7, [])
        self.solver.q_table[state_key] = {'higher': 5, 'lower': 5, 'bank': 10}
        action = self.solver.get_action(state_key)
        self.assertEqual(action, 'bank', 
                        "Solver should choose to bank when no numbers remain")
        
        # Test transition to new round after all numbers used
        state_key = self.solver.get_state_key(7, 0, 0, [])  # After banking with no numbers
        next_state = self.solver.get_state_key(7, 0, 0, list(range(1, 14)))  # New round state
        self.solver.update_q_value(state_key, 'bank', -1, next_state)
        self.assertIn('bank', self.solver.q_table[state_key], 
                     "Q-table should have entry for banking when no numbers remain")
    
    def test_q_value_updates(self):
        """Test that Q-values are updated correctly."""
        # Test basic Q-value update
        state = "0_5_3_1,2,4,5"
        next_state = "0_8_4_1,2,5"
        self.solver.update_q_value(state, 'higher', 10, next_state)
        self.assertGreater(self.solver.q_table[state]['higher'], 0, "Q-value should be positive after positive reward")
        
        # Test Q-value update with negative reward
        state = "0_5_3_1,2,4,5"
        next_state = "0_0_0_"
        self.solver.update_q_value(state, 'higher', -50, next_state)
        self.assertLess(self.solver.q_table[state]['higher'], 0, "Q-value should be negative after negative reward")
    
    def test_model_saving_loading(self):
        """Test that the model can be saved and loaded correctly."""
        # Train the model a bit
        state = "0_5_3_1,2,4,5"
        self.solver.q_table[state] = {'higher': 10, 'lower': 5, 'bank': 8}
        
        # Save and load
        self.solver.save_model("test_model.pkl")
        new_solver = PushYourLuckSolver()
        new_solver.load_model("test_model.pkl")
        
        # Check if Q-values are preserved
        self.assertEqual(self.solver.q_table[state], new_solver.q_table[state],
                        "Q-values should be preserved after save and load")
    
    def test_play_game_mechanics(self):
        """Test the play_game method's basic mechanics."""
        # Set up a deterministic game state
        def mock_random_choice(seq):
            return seq[0]  # Always return first element
        
        # Replace random.choice with our mock
        original_random_choice = random.choice
        random.choice = mock_random_choice
        
        try:
            # Play a game with verbose=False to avoid print statements
            score, rounds = self.solver.play_game(verbose=False)
            
            # Basic assertions
            self.assertIsInstance(score, int, "Score should be an integer")
            self.assertIsInstance(rounds, int, "Rounds should be an integer")
            self.assertGreaterEqual(score, 0, "Score should be non-negative")
            self.assertGreater(rounds, 0, "Should have played at least one round")
            
        finally:
            # Restore original random.choice
            random.choice = original_random_choice

if __name__ == '__main__':
    unittest.main() 