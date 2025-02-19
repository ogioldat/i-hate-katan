import unittest
from tests.utils import TicTacToeGameStrategy
from simulation.mcts import MonteCarloTreeSearch


class TestMCTS(unittest.TestCase):
    def test_moves_expansion(self):
        strategy = TicTacToeGameStrategy()

        mcts = MonteCarloTreeSearch(
            game_strategy=strategy, simulations=1, max_depth=100
        )
        mcts.run()


if __name__ == "__main__":
    unittest.main()
