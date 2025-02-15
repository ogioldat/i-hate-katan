from lib.game import GameStrategy, GameResult, GameMoveNode, NotTerminalNodeError

"""
 0 | 1 | 2
---|---|---
 3 | 4 | 5
---|---|---
 6 | 7 | 8
 
Playing as x, o's are randomly set
"""


class TicTatToeGameStrategy(GameStrategy):
    def __init__(self):
        self.__state = [None] * 9

        self.__winning_moves = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        self.__key_seq = 1

    def expand_moves(self, node: GameMoveNode) -> None:
        for idx in range(self.__state):
            el = self.__state[idx]
            if el is not None:
                node.append(key=self.__key_seq, label="")

    def no_moves_left(self, node: GameMoveNode) -> bool:
        return True

    def random_game(self, node: GameMoveNode) -> GameResult:
        if not self.is_terminal_move(node):
            raise NotTerminalNodeError
