import unittest
from tests.utils import TicTacToeGameStrategy
from simulation import MonteCarloTreeSearch, FirstChildNodeSelectionPolicy


class TestMCTS(unittest.TestCase):
    def test_moves_expansion(self):
        strategy = TicTacToeGameStrategy()

        mcts = MonteCarloTreeSearch(
            game_strategy=strategy,
            simulations=1,
            max_depth=100,
            selection_policy=FirstChildNodeSelectionPolicy(),
        )
        mcts.run()


if __name__ == "__main__":
    unittest.main()
