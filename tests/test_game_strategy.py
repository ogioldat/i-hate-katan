import unittest
from tictactoe_game_strategy import TicTatToeGameStrategy
from lib.game import GameMoveNode


class TestGameStrategy(unittest.TestCase):
    def test_moves_expansion(self):
        strategy = TicTatToeGameStrategy()

        root_node_key = TicTatToeGameStrategy.initial_state_hash()
        root_node = GameMoveNode(key=root_node_key)

        strategy.expand_moves(root_node)

        assert len(root_node.children) == 9

    def test_moves_expansion_determinism(self):
        strategy = TicTatToeGameStrategy()

        root_node_key = TicTatToeGameStrategy.initial_state_hash()
        root_node = GameMoveNode(key=root_node_key)

        strategy.expand_moves(root_node)
        strategy.expand_moves(root_node)

        assert len(root_node.children) == 9


if __name__ == "__main__":
    unittest.main()
