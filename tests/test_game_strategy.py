import unittest
from tictactoe_game_strategy import TicTatToeGameStrategy
from lib.game import GameMoveNode


class TestGameStrategy(unittest.TestCase):
    def test_moves_expansion(self):
        strategy = TicTatToeGameStrategy()
        root_node = GameMoveNode(key=0)

        strategy.expand_moves(root_node)
        strategy.pretty_print_node(root_node)

    # def test_moves_expansion_determinism(self):
    #     strategy = TicTatToeGameStrategy()
    #     root_node = GameMoveNode(key=0)


if __name__ == "__main__":
    unittest.main()
