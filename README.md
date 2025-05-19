# Push Your Luck Game

A Python implementation of the Push Your Luck game show with both a playable version and an AI solver that learns optimal strategies.

## Game Versions

1. **Single Player** (`push_your_luck_single.py`)
   - Play against yourself
   - Try to reach 100 points
   - Bank your points or risk them for more
   - Uses a spinner with numbers 1-13

2. **Simultaneous Multiplayer** (`push_your_luck_simultaneous.py`)
   - 2-4 players
   - All players guess for each target number
   - First to reach 100 points wins
   - Uses a spinner with numbers 1-13

3. **AI Solver** (`push_your_luck_solver.py`)
   - Uses Q-learning to find optimal strategies
   - Learns to balance risk and reward
   - Can save and load learned strategies
   - Includes comprehensive test suite
   - Uses a spinner with numbers 1-13

4. **Mixed Game** (`push_your_luck_mixed.py`)
   - Play against multiple computer players with different strategies
   - Features:
     - Human player
     - AI Solver (uses trained Q-learning model)
     - Safe Player (always banks)
     - Probability Player (makes decisions based on >50% probability)
     - Expected Value Player (makes decisions based on expected payoffs)
   - First to reach 100 points wins
   - Uses a spinner with numbers 1-13

## How to Play

### Human Players
1. Run the single player version:
   ```
   python push_your_luck_single.py
   ```
   or the multiplayer version:
   ```
   python push_your_luck_simultaneous.py
   ```
   or the mixed game version:
   ```
   python push_your_luck_mixed.py
   ```

2. Follow the on-screen instructions to:
   - Enter number of players (for multiplayer)
   - Enter player names
   - Make your guesses (higher/lower/bank)

### AI Solver
1. Run the solver:
   ```
   python push_your_luck_solver.py
   ```
   This will:
   - Try to load any existing trained model
   - Train for 10,000 episodes
   - Save the trained model
   - Play 5 demonstration games

2. Run the tests:
   ```
   python -m unittest test_push_your_luck_solver.py
   ```

## Game Rules

- Each round starts with a target number from the spinner
- Players guess if the next number will be higher or lower
- Correct guesses add points to your bank
- Bank your points to add them to your score
- Wrong guesses result in a bust (lose your bank)
- First to reach the target score wins!
  - Single player: 50 points
  - Multiplayer: 100 points
  - AI solver: 50 points
  - Mixed game: 100 points

## AI Solver Details

The solver uses Q-learning to develop strategies for playing the game. Key features:

### Learning Parameters
- Learning rate: 0.1
- Discount factor: 0.95
- Exploration rate: Starts at 1.0, decays to 0.01
- Exploration decay: 0.995

### Reward Structure
- Correct guess: +3
- Busting: -2
- Round penalty: -1
- Winning: +100

### Model Persistence
- Trained models are saved to `push_your_luck_model.pkl`
- The solver can continue learning from previous training sessions
- Models can be shared between different runs

### Computer Players in Mixed Game
The mixed game version includes four different computer players:

1. **AI Solver**
   - Uses the trained Q-learning model
   - Makes decisions based on learned optimal strategies
   - Requires a trained model file (`push_your_luck_model.pkl`)

2. **Safe Player**
   - Always chooses to bank
   - Conservative strategy that minimizes risk
   - Good baseline for comparison

3. **Probability Player**
   - Calculates probability of higher/lower
   - Chooses higher/lower if probability > 50%
   - Banks if neither option has >50% probability
   - Uses pure mathematical strategy

4. **Expected Value Player**
   - Makes decisions based on weighted expected payoffs
   - Calculates expected value for both higher and lower
   - Banks when:
     - Expected payoffs are low relative to current bank
     - Expected payoffs are very close to each other
     - Current bank is high relative to expected payoffs
   - Otherwise chooses the option with higher expected payoff
   - Balances risk and reward using probability-weighted values

### Testing
The project includes two test suites:

1. **Solver Tests** (`test_push_your_luck_solver.py`)
   - Verifies basic game mechanics
   - Tests edge cases (target numbers, available numbers)
   - Validates banking strategies
   - Checks score and bank combinations
   - Tests model saving and loading
   - Verifies Q-value updates

2. **Mixed Game Tests** (`test_push_your_luck_mixed.py`)
   - Tests all computer player strategies:
     - Safe Player: Verifies always-bank behavior
     - Probability Player: Tests probability-based decisions
     - Expected Value Player: Validates expected payoff calculations
   - Covers edge cases:
     - Smallest/largest target numbers
     - Equal probability scenarios
     - High/low expected payoffs
   - Tests banking conditions:
     - Close expected payoffs
     - Low payoffs relative to bank
     - High bank relative to payoffs
   - Verifies game mechanics:
     - Round initialization
     - Spinner state management
     - Player state handling

Run the tests with:
```
# Test the solver
python -m unittest test_push_your_luck_solver.py

# Test the mixed game
python -m unittest test_push_your_luck_mixed.py
```

## File Descriptions

- `push_your_luck_single.py`: Single player game implementation
- `push_your_luck_simultaneous.py`: Multiplayer game implementation
- `push_your_luck_solver.py`: AI solver implementation
- `push_your_luck_mixed.py`: Mixed game with human and computer players
- `test_push_your_luck_solver.py`: Test suite for the solver
- `test_push_your_luck_mixed.py`: Test suite for the mixed game
- `push_your_luck_model.pkl`: Saved model file (created after training)

## Notes

- The solver's strategy can be adjusted by modifying the reward structure
- Different spinner ranges are used for different game versions
- The solver's exploration rate ensures it tries different strategies
- The test suites help ensure all components work as intended
- The model file allows the solver to continue learning across sessions
- The mixed game provides an interesting way to compare different strategies
- **Make sure to train the AI solver before playing the mixed game**
- The Expected Value Player's banking thresholds can be adjusted:
  - `bank_threshold`: Bank if expected payoffs are below this fraction of current bank (default: 0.8)
  - `payoff_threshold`: Bank if payoffs are within this fraction of each other (default: 0.1)