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

    def __eq__(self, other: GameStateShape) -> bool:
        return self == other

    def __hash__(self):
        return hash(self.moves)


@dataclass(frozen=True)
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
    __WINNING_MOVES = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    __INITIAL_STATE: TicTacToeStateShape = TicTacToeStateShape(moves=(0,) * 9)

    def __init__(self):
        super().__init__()
        self.__storage = super()._create_state_storage(
            storage_shape=TicTacToeStateShape
        )

    @staticmethod
    def move_from_state(state: TicTacToeStateShape, player: Players, move_idx: int):
        loose_moves = list(state.moves)
        loose_moves[move_idx] = player

        return tuple(loose_moves)

    def expand_moves(self, node: GameMoveNode) -> None:
        if node.is_root():
            self.__storage.set(node.key, TicTatToeGameStrategy.__INITIAL_STATE)
            expand_from_state = self.__storage.get(node.key)
        else:
            expand_from_state = self.__storage.get(node.parent.key)

        for move_idx, _ in enumerate(expand_from_state.moves):
            move = expand_from_state.moves[move_idx]

            if move == Players.NONE:
                next_move_state = TicTatToeGameStrategy.move_from_state(
                    expand_from_state, Players.P1, move_idx
                )
                node_key = TicTatToeGameStrategy.state_hash(next_move_state)

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
        state = self.__storage.get(node.key).moves

        print(f"""
            {state[0]} | {state[1]} | {state[2]}
           ---|---|---
            {state[3]} | {state[4]} | {state[5]}
           ---|---|---
            {state[6]} | {state[7]} | {state[8]}
        """)

    @classmethod
    def initial_state_hash(cls) -> int:
        return cls.state_hash(cls.__INITIAL_STATE)
