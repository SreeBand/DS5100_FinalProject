import numpy as np
import pandas as pd

class Die:
    """
    A Die has N sides, each with a unique symbol (numeric or string), and associated weights.
    The die can be rolled to randomly select a face based on these weights.

    By default, all weights are 1.0, representing a fair die.
    Weights can be modified after initialization.

    Attributes:
        __df (pd.DataFrame): Private dataframe storing faces and their weights.
    """

    def __init__(self, faces: np.ndarray):
        """
        Initializes a Die object with unique faces.

        Parameters:
            faces (np.ndarray): A NumPy array of unique face symbols (numeric or strings).

        Raises:
            TypeError: If faces is not a NumPy array.
            ValueError: If faces are not unique.
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be provided as a NumPy array.")
        if len(faces) != len(set(faces)):
            raise ValueError("Faces must contain unique values.")
        
        self.__df = pd.DataFrame({
            'face': faces,
            'weight': np.ones(len(faces))
        }).set_index('face')

    def change_weight(self, face, new_weight):
        """
        Changes the weight of a specific face.

        Parameters:
            face: The face value whose weight is to be changed.
            new_weight: The new weight (float or int, must be non-negative).

        Raises:
            IndexError: If the face is not found.
            TypeError: If new_weight is not numeric or castable to float.
            ValueError: If new_weight is negative.

        State Changes:
            Updates the weight for the specified face.
        """
        if face not in self.__df.index:
            raise IndexError(f"Face '{face}' not found in die faces.")
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise TypeError("New weight must be numeric or castable to float.")
        if new_weight < 0:
            raise ValueError("Weight must be non-negative.")
        
        self.__df.at[face, 'weight'] = new_weight

    def roll(self, num_rolls=1):
        """
        Rolls the die a specified number of times.

        Parameters:
            num_rolls (int): Number of times to roll the die (default is 1).

        Returns:
            list: A list of outcomes from the rolls.

        Raises:
            ValueError: If num_rolls is not a positive integer.

        Does not store results internally.
        """
        if not isinstance(num_rolls, int) or num_rolls <= 0:
            raise ValueError("Number of rolls must be a positive integer.")
        faces = self.__df.index.to_list()
        weights = self.__df['weight'].to_list()
        result = list(np.random.choice(faces, size=num_rolls, p=np.array(weights) / sum(weights)))
        return result

    def show(self):
        """
        Displays the current state of the die.

        Returns:
            pd.DataFrame: A copy of the dataframe showing faces and their weights.
        """
        return self.__df.copy()

class Game:
    """
    A Game consists of rolling one or more similar Die objects multiple times.
    It records the outcomes of the most recent play.

    Attributes:
        __dice (list): List of Die objects.
        __results (pd.DataFrame): Private dataframe storing latest play results.
    """

    def __init__(self, dice_list):
        """
        Initializes a Game with a list of Die objects.

        Parameters:
            dice_list (list): A list containing one or more Die objects.

        Raises:
            ValueError: If dice_list is empty or not a list.
        """
        if not isinstance(dice_list, list) or len(dice_list) == 0:
            raise ValueError("Must provide a non-empty list of dice.")
        self.__dice = dice_list
        self.__results = None

    def play(self, num_rolls):
        """
        Rolls all dice a specified number of times.

        Parameters:
            num_rolls (int): Number of times to roll the dice.

        Raises:
            ValueError: If num_rolls is not a positive integer.

        State Changes:
            Stores the results of the play in a private dataframe.
        """
        if not isinstance(num_rolls, int) or num_rolls <= 0:
            raise ValueError("Number of rolls must be a positive integer.")
        
        rolls = {}
        for i, die in enumerate(self.__dice):
            rolls[i] = die.roll(num_rolls)
        
        self.__results = pd.DataFrame(rolls)
        self.__results.index.name = "Roll Number"

    def show(self, form='wide'):
        """
        Displays the results of the most recent play.

        Parameters:
            form (str): 'wide' (default) or 'narrow' format.

        Returns:
            pd.DataFrame: Copy of the play results dataframe.

        Raises:
            ValueError: If no game has been played or invalid format is passed.
        """
        if self.__results is None:
            raise ValueError("No game has been played yet.")
        
        if form == 'wide':
            return self.__results.copy()
        elif form == 'narrow':
            narrow_df = self.__results.stack()
            narrow_df.index.set_names(['Roll Number', 'Die Number'], inplace=True)
            return narrow_df.to_frame('Outcome')
        else:
            raise ValueError("Invalid form. Use 'wide' or 'narrow'.")

class Analyzer:
    """
    Analyzer computes descriptive statistics from a single Game's results.

    Provides methods to compute jackpots, face counts, combinations, and permutations.
    """

    def __init__(self, game):
        """
        Initializes the Analyzer with a Game object.

        Parameters:
            game (Game): A Game object containing play results.

        Raises:
            ValueError: If input is not a Game object.
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        self.game = game
        self.results = game.show('wide')

    def jackpot(self):
        """
        Computes the number of jackpots (all dice showing the same face in a roll).

        Returns:
            int: Number of jackpots found.
        """
        jackpots = self.results.apply(lambda row: len(set(row)) == 1, axis=1)
        return int(jackpots.sum())

    def face_counts_per_roll(self):
        """
        Counts occurrences of each face per roll.

        Returns:
            pd.DataFrame: DataFrame with roll numbers as index, face values as columns, and counts in cells.
        """
        counts_list = []
        unique_faces = pd.unique(self.results.values.ravel())
        for _, row in self.results.iterrows():
            counts = pd.Series(row).value_counts()
            counts = counts.reindex(unique_faces, fill_value=0)
            counts_list.append(counts)
        face_counts_df = pd.DataFrame(counts_list)
        face_counts_df.index = self.results.index
        face_counts_df.index.name = 'Roll Number'
        return face_counts_df

    def combo_count(self):
        """
        Computes distinct combinations (order-independent) of faces rolled and their counts.

        Returns:
            pd.DataFrame: DataFrame with MultiIndex of combinations and a count column.
        """
        combos = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combos.value_counts().to_frame('Count')
        combo_counts.index.name = 'Combination'
        return combo_counts

    def permutation_count(self):
        """
        Computes distinct permutations (order-dependent) of faces rolled and their counts.

        Returns:
            pd.DataFrame: DataFrame with MultiIndex of permutations and a count column.
        """
        perms = self.results.apply(lambda row: tuple(row), axis=1)
        perm_counts = perms.value_counts().to_frame('Count')
        perm_counts.index.name = 'Permutation'
        return perm_counts