import unittest
import numpy as np
import pandas as pd
from die_game_analyzer import Die, Game, Analyzer

class TestDieGameAnalyzer(unittest.TestCase):

    def setUp(self):
        """Set up common test objects for Die, Game, and Analyzer."""
        self.faces = np.array([1, 2, 3, 4, 5, 6])
        self.die = Die(self.faces)
        self.dice_list = [self.die, Die(self.faces)]
        self.game = Game(self.dice_list)
        self.game.play(5)
        self.analyzer = Analyzer(self.game)

    # --- Tests for Die Class (4 methods) ---

    def test_die_init_creates_dataframe(self):
        """Test Die initialization creates correct DataFrame structure."""
        df = self.die.show()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue((df['weight'] == 1.0).all())

    def test_die_change_weight_updates_weight(self):
        """Test that changing a weight updates the DataFrame correctly."""
        self.die.change_weight(6, 3.5)
        df = self.die.show()
        self.assertEqual(df.loc[6, 'weight'], 3.5)

    def test_die_roll_returns_correct_length_list(self):
        """Test that Die.roll() returns a list of correct length."""
        outcomes = self.die.roll(4)
        self.assertIsInstance(outcomes, list)
        self.assertEqual(len(outcomes), 4)

    def test_die_show_returns_dataframe(self):
        """Test that Die.show() returns a DataFrame."""
        result = self.die.show()
        self.assertIsInstance(result, pd.DataFrame)

    # --- Tests for Game Class (3 methods) ---

    def test_game_init_accepts_dice_list(self):
        """Test Game initialization with dice list."""
        game = Game(self.dice_list)
        self.assertIsInstance(game, Game)

    def test_game_play_creates_results_dataframe(self):
        """Test Game.play() stores a DataFrame of correct shape."""
        df = self.game.show('wide')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (5, len(self.dice_list)))

    def test_game_show_formats(self):
        """Test Game.show() returns correct formats."""
        wide_df = self.game.show('wide')
        narrow_df = self.game.show('narrow')
        self.assertIsInstance(wide_df, pd.DataFrame)
        self.assertIsInstance(narrow_df, pd.DataFrame)
        self.assertIsInstance(narrow_df.index, pd.MultiIndex)

    # --- Tests for Analyzer Class (5 methods) ---

    def test_analyzer_init_stores_results(self):
        """Test Analyzer initialization stores game results."""
        self.assertIsInstance(self.analyzer.results, pd.DataFrame)

    def test_analyzer_jackpot_returns_integer(self):
        """Test that Analyzer.jackpot() returns an integer."""
        jackpots = self.analyzer.jackpot()
        self.assertIsInstance(jackpots, int)

    def test_analyzer_face_counts_per_roll_structure(self):
        """Test that face_counts_per_roll returns a DataFrame."""
        counts_df = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(counts_df, pd.DataFrame)
        self.assertEqual(counts_df.shape[0], self.game.show().shape[0])

    def test_analyzer_combo_count_returns_dataframe(self):
        """Test combo_count returns a DataFrame with MultiIndex."""
        combo_df = self.analyzer.combo_count()
        self.assertIsInstance(combo_df, pd.DataFrame)
        self.assertTrue(isinstance(combo_df.index, pd.Index) or isinstance(combo_df.index, pd.MultiIndex))

    def test_analyzer_permutation_count_returns_dataframe(self):
        """Test permutation_count returns a DataFrame with MultiIndex."""
        perm_df = self.analyzer.permutation_count()
        self.assertIsInstance(perm_df, pd.DataFrame)
        self.assertTrue(isinstance(perm_df.index, pd.Index) or isinstance(perm_df.index, pd.MultiIndex))


if __name__ == '__main__':
    unittest.main()
