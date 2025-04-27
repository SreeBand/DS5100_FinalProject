# Monte Carlo Simulator:

# Metadata:

**Author**: Sree Prabhav Bandakavi  
**Project Name**: Monte Carlo Simulator 

****
# Synopsis:  
 This project allows users to do the following:  
 - Create a Dice with ***N*** faces and ***W*** weights 
 - Play a game consisting of rolling one or more similar dice one or more times. 
 - An analyzer which will take the results of a single game and compute various decriptive statistics about it
 
 Demo:  
 
 ```python
# Install numpy and pandas if needed

# Import classes
from die_game_analyzer import Die, Game, Analyzer
import numpy as np

# 1. Create Dice
faces = np.array([1, 2, 3, 4, 5, 6])
die1 = Die(faces)
die2 = Die(faces)
die1.change_weight(6, 5.0)  # Make face '6' heavier

# 2. Play a Game
game = Game([die1, die2])
game.play(10)  # Roll both dice 10 times
print(game.show('wide'))

# 3. Analyze the Game
analyzer = Analyzer(game)
print("Jackpots:", analyzer.jackpot())
print(analyzer.face_counts_per_roll())
print(analyzer.combo_count())
print(analyzer.permutation_count())
 ```
 
 
 ****
# API description:
 
## Die - Class
A die has $N$ sides, or “faces”, and $W$ weights, and can be rolled to select a face.
 
1. **Die(faces: np.ndarray)**  
 Initializes a Die object with unique faces.  
 - Parameters:
     - faces (np.ndarray): A NumPy array of unique face symbols (numeric or strings).  
 - Raises: 
    - TypeError, ValueError

2. **change_weight(face, new_weight)**    
Changes the weight of a specific face.  
- Parameters:
    - face: The face value whose weight is to be changed.
    - new_weight: The new weight (float or int, must be non-negative).  
- Raises:
    - IndexError, TypeError, ValueError
    
3. **roll(num_rolls=1)**    
Rolls the die  
- Parameters: 
    - num_rolls (int): Number of times to roll the die (default is 1).
- Returns: 
    - list: A list of outcomes from the rolls.  
- Raises:
    - ValueError
4. **show()**  
Displays the current state of the die.
- Returns:
    - pd.DataFrame: A copy of the dataframe showing faces and their weights.
    
## Game - Class  
A Game consists of rolling one or more similar Die objects multiple times. It records the outcomes of the most recent play.  
1. **Game(dice_list: list)**  
Initializes a Game with a list of Die objects.
 - Parameters: 
     - dice_list (list): A list containing one or more Die objects.
 - Raises:
      - ValueError  
2. **play(num_rolls)**   
Rolls all dice  
- Parameters:
    - num_rolls (int): Number of times to roll.
- Raises: 
    - ValueError
- State Change:
    - Stores results internally.  
3. **show(form='wide')**  
Displays play results.
- Parameters:
    - form (str, default='wide'): 'wide' or 'narrow'.
- Returns: 
    - pd.DataFrame
- Raises: 
    - ValueError 
    
## Analyzer - Class    
 Analyzer computes descriptive statistics from a single Game's results. Provides methods to compute jackpots, face counts, combinations, and permutations.  
 
1. **Analyzer(game: Game)**  
Initializes the Analyzer.
- Parameters:
    - game (Game): A completed Game object.
- Raises:
    - ValueError  
2. **jackpot()**  
Counts rolls where all dice show the same face.
- Returns: 
    - int (number of jackpots)  
3. **combo_count()**  
Counts distinct combinations (order-independent).
- Returns: 
    - pd.DataFrame (MultiIndex of combinations + counts)
4. **permutation_count()**  
Counts distinct permutations (order-dependent).
- Returns: 
    - pd.DataFrame (MultiIndex of permutations + counts)