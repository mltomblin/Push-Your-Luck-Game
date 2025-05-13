# Push Your Luck Game

A Python implementation of the Push Your Luck game show. Players spin a wheel (numbered 1-4) and guess if the next number will be higher or lower than the target number.

## Game Versions

1. **Single Player** (`push_your_luck_single.py`)
   - Play against yourself
   - Try to reach 50 points
   - Bank your points or risk them for more

2. **Simultaneous Multiplayer** (`push_your_luck_simultaneous.py`)
   - 2-4 players
   - All players guess for each target number
   - First to reach 100 points wins

## How to Play

1. Run the game:
   ```
   python push_your_luck_single.py
   ```
   or
   ```
   python push_your_luck_simultaneous.py
   ```

2. Follow the on-screen instructions to:
   - Enter number of players (for multiplayer)
   - Enter player names
   - Make your guesses (higher/lower/bank)

## Game Rules

- Each round starts with a target number
- Guess if the next number will be higher or lower
- Correct guesses add points to your bank
- Bank your points to add them to your score
- Wrong guesses result in a bust (lose your bank)
- First to reach the target score (50 for single player, 100 for multiplayer) wins!