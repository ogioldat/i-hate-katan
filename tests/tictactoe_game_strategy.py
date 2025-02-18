from dataclasses import dataclass
from lib.game import (
    GameStrategy,
    GameResult,
    GameMoveNode,
    NotTerminalNodeError,
    GameStateShape,
)
from typing import Tuple


@dataclass
class TicTacToeStateShape(GameStateShape):
    moves: Tuple[int, int, int, int, int, int, int, int, int]


@dataclass
class Players:
    NONE = 0
    P1 = 1


"""
 0 | 1 | 2
---|---|---
 3 | 4 | 5
---|---|---
 6 | 7 | 8
 
This is a simplified version of TicTacToe, for testing purposes, only one player is supported,
the goal is to build decision tree of possible moves the player can make to win the game.
"""


class TicTatToeGameStrategy(GameStrategy):
    WINNING_MOVES = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    INITIAL_MOVES = (0,) * 9

    def __init__(self):
        self.__storage = super().create_state_storage(storage_shape=TicTacToeStateShape)

    @staticmethod
    def move_from_state(state: TicTacToeStateShape, player: Players, move: int):
        loose_moves = list(state.moves)
        loose_moves[move] = player

        return tuple(loose_moves)

    def expand_moves(self, node: GameMoveNode) -> None:
        if node.is_root():
            self.__storage.set(node.key, TicTatToeGameStrategy.INITIAL_MOVES)
            return

        parent_state = self.__storage.get(node.parent.key)

        for move in parent_state.moves:
            if move == Players.NONE:
                next_move_state = TicTatToeGameStrategy.move_from_state(
                    node.state, Players.P1, move
                )
                node_key = super().next_key()

                node.append(key=node_key)

                self.__storage.set(key=node_key, value=next_move_state)

            if move == Players.P1:
                pass

    def no_moves_left(self, node: GameMoveNode) -> bool:
        return True

    def random_game(self, node: GameMoveNode) -> GameResult:
        if not self.is_terminal_move(node):
            raise NotTerminalNodeError

    def pretty_print_node(self, node: GameMoveNode):
        move = self.__storage.get(node.key)
        print(f"key={node.key}")
        print(f"""
            {move[0]} | {move[1]} | {move[2]}
           ---|---|---
            {move[3]} | {move[4]} | {move[5]}
           ---|---|---
            {move[6]} | {move[7]} | {move[8]}
        """)
