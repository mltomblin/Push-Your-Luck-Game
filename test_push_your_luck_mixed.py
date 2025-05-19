import unittest
from push_your_luck_mixed import (
    Player, SafePlayer, ProbabilityPlayer, ExpectedValuePlayer, AIPlayer,
    MixedPushYourLuckGame
)

class TestComputerPlayers(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.safe_player = SafePlayer("Safe Test")
        self.prob_player = ProbabilityPlayer("Prob Test")
        self.ev_player = ExpectedValuePlayer("EV Test")
        # Note: AIPlayer tests are limited since they require a trained model
    
    def test_safe_player(self):
        """Test that SafePlayer always banks."""
        test_cases = [
            (5, [1, 2, 3, 4, 6, 7, 8, 9, 10]),  # Normal case
            (1, [2, 3, 4, 5, 6, 7, 8, 9, 10]),  # Smallest target
            (10, [1, 2, 3, 4, 5, 6, 7, 8, 9]),  # Largest target
            (5, [5, 5, 5, 5, 5]),  # All same numbers
        ]
        
        for target, numbers in test_cases:
            with self.subTest(target=target, numbers=numbers):
                guess = self.safe_player.get_guess(target, numbers)
                self.assertEqual(guess, 'bank', 
                    f"SafePlayer should always bank, got {guess} for target {target} with numbers {numbers}")
    
    def test_probability_player(self):
        """Test ProbabilityPlayer's decision making."""
        test_cases = [
            # (target, numbers, expected_guess, description)
            (5, [1, 2, 3, 4, 6, 7, 8, 9, 10], 'higher', 
             "Should choose higher when probability > 50%"),
            (5, [1, 2, 3, 4, 6, 7], 'lower',
             "Should choose lower when probability > 50%"),
            (5, [4, 5, 6], 'bank',
             "Should bank when neither option has >50% probability"),
            (1, [2, 3, 4, 5, 6, 7, 8, 9, 10], 'higher',
             "Should choose higher when target is smallest"),
            (10, [1, 2, 3, 4, 5, 6, 7, 8, 9], 'lower',
             "Should choose lower when target is largest"),
        ]
        
        for target, numbers, expected, description in test_cases:
            with self.subTest(target=target, numbers=numbers, description=description):
                guess = self.prob_player.get_guess(target, numbers)
                self.assertEqual(guess, expected,
                    f"ProbabilityPlayer {description}. Got {guess} for target {target} with numbers {numbers}")
    
    def test_expected_value_player(self):
        """Test ExpectedValuePlayer's decision making."""
        test_cases = [
            # (target, numbers, expected_guess, description)
            # Edge cases
            (1, [2, 3, 4, 5, 6, 7, 8, 9, 10], 'higher',
             "Should choose higher when target is smallest"),
            (10, [1, 2, 3, 4, 5, 6, 7, 8, 9], 'lower',
             "Should choose lower when target is largest"),
            (5, [1, 2, 3, 4, 6, 7, 8, 9, 10], 'higher',
             "Should choose higher when expected payoff is higher"),
            (5, [1, 2, 3, 4, 6], 'lower',
             "Should choose lower when expected payoff is higher"),
            # Banking cases
            (5, [4, 5, 6], 'bank',
             "Should bank when expected payoffs are close"),
            (5, [1, 2, 3, 4, 6, 7, 8, 9, 10], 'bank',
             "Should bank when current bank is high relative to expected payoffs"),
        ]
        
        for target, numbers, expected, description in test_cases:
            with self.subTest(target=target, numbers=numbers, description=description):
                # Set bank to a high value for banking test cases
                self.ev_player.bank = 20 if expected == 'bank' else 0
                guess = self.ev_player.get_guess(target, numbers)
                self.assertEqual(guess, expected,
                    f"ExpectedValuePlayer {description}. Got {guess} for target {target} with numbers {numbers}")
    
    def test_expected_value_player_banking_conditions(self):
        """Test ExpectedValuePlayer's banking conditions."""
        player = ExpectedValuePlayer("EV Test", bank_threshold=0.8, payoff_threshold=0.1)
        
        # Test banking when payoffs are close
        player.bank = 10
        numbers = [8, 9, 10, 11, 12]  # Close numbers around target
        guess = player.get_guess(10, numbers)
        self.assertEqual(guess, 'bank',
            "Should bank when expected payoffs are close to each other")
        
        # Test banking when payoffs are low relative to bank
        player.bank = 20
        numbers = [1, 2, 3, 4, 5]  # Low numbers
        guess = player.get_guess(3, numbers)
        self.assertEqual(guess, 'bank',
            "Should bank when expected payoffs are low relative to current bank")
        
        # Test banking when bank is high relative to payoffs
        player.bank = 30
        numbers = [1, 2, 3, 4, 5]  # Low numbers
        guess = player.get_guess(3, numbers)
        self.assertEqual(guess, 'bank',
            "Should bank when current bank is high relative to expected payoffs")
    
    def test_mixed_game_mechanics(self):
        """Test basic game mechanics with computer players."""
        game = MixedPushYourLuckGame()
        
        # Add computer players
        game.add_player(SafePlayer("Safe Test"))
        game.add_player(ProbabilityPlayer("Prob Test"))
        game.add_player(ExpectedValuePlayer("EV Test"))
        
        # Test round initialization
        game.start_new_round()
        self.assertIn(game.target_num, game.main_spinner,
            "Target number should be from main spinner")
        self.assertEqual(len(game.round_spinner), len(game.main_spinner) - 1,
            "Round spinner should have one less number than main spinner")
        self.assertNotIn(game.target_num, game.round_spinner,
            "Target number should not be in round spinner")
        
        # Test player state initialization
        for player in game.players:
            self.assertTrue(player.is_active,
                "Players should be active at start of round")
            self.assertEqual(player.bank, game.target_num,
                "Player bank should be initialized to target number")

if __name__ == '__main__':
    unittest.main() 