import unittest
from tests.utils import TicTacToeGameStrategy
from lib.game import GameMoveNode


class TestGameStrategy(unittest.TestCase):
    def test_moves_expansion(self):
        strategy = TicTacToeGameStrategy()

        root_node_key = TicTacToeGameStrategy.initial_state_hash()
        root_node = GameMoveNode(key=root_node_key)

        strategy.expand_moves(root_node)

        assert len(root_node.children) == 9

    def test_moves_expansion_determinism(self):
        strategy = TicTacToeGameStrategy()

        root_node_key = TicTacToeGameStrategy.initial_state_hash()
        root_node = GameMoveNode(key=root_node_key)

        strategy.expand_moves(root_node)
        strategy.expand_moves(root_node)

        assert len(root_node.children) == 9


if __name__ == "__main__":
    unittest.main()
