from dataclasses import dataclass
from lib.game import (
    GameStrategy,
    GameResult,
    GameMoveNode,
    NotTerminalNodeError,
    GameStateShape,
)
from typing import Tuple, List


@dataclass(frozen=True)
class Player:
    NONE = 0
    P1 = 1


@dataclass
class TicTacToeStateShape(GameStateShape):
    moves: Tuple[Player, Player, Player, Player, Player, Player, Player, Player, Player]

    def __eq__(self, other: GameStateShape) -> bool:
        return self == other

    def __hash__(self):
        return hash(self.moves)


"""
 0 | 1 | 2
---|---|---
 3 | 4 | 5
---|---|---
 6 | 7 | 8
 
This is a simplified version of TicTacToe, for testing purposes, only one player is supported,
the goal is to build decision tree of possible moves the player can make to win the game.
"""


class TicTacToeGameStrategy(GameStrategy):
    __WINNING_MOVES: List[Tuple[int, int, int]] = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    __INITIAL_STATE: TicTacToeStateShape = TicTacToeStateShape(moves=(0,) * 9)

    def __init__(self):
        super().__init__()
        self.__storage = super()._create_state_storage(
            storage_shape=TicTacToeStateShape
        )

    @staticmethod
    def move_from_state(
        state: TicTacToeStateShape, player: Player, move_idx: int
    ) -> TicTacToeStateShape:
        loose_moves = list(state.moves)
        loose_moves[move_idx] = player

        return TicTacToeStateShape(moves=tuple(loose_moves))

    def expand_moves(self, node: GameMoveNode) -> None:
        if node.is_root():
            self.__storage.set(node.key, TicTacToeGameStrategy.__INITIAL_STATE)
            expand_from_state = self.__storage.get(node.key)
        else:
            expand_from_state = self.__storage.get(node.parent.key)

        for move_idx, _ in enumerate(expand_from_state.moves):
            move = expand_from_state.moves[move_idx]

            if move == Player.NONE:
                next_move_state = TicTacToeGameStrategy.move_from_state(
                    expand_from_state, Player.P1, move_idx
                )
                node_key = hash(next_move_state)

                if node_key == "4423490485614069943":
                    pass

                if node.key == node_key:
                    continue

                node.append(key=node_key)
                self.__storage.set(key=node_key, value=next_move_state)

            if move == Player.P1:
                pass

    def no_moves_left(self, node: GameMoveNode) -> bool:
        moves = self.__storage.get(node.key).moves

        for winning_move in TicTacToeGameStrategy.__WINNING_MOVES:
            [w_idx_0, w_idx_1, w_idx_2] = winning_move

            if moves[w_idx_0] and moves[w_idx_1] and moves[w_idx_2]:
                print("Found winner: ", node)

                node.add_wins()

                return True

        for idx, move in enumerate(moves):
            if move is Player.NONE:
                return False

            if len(moves) == idx + 1:
                return True

        return False

    def random_game(self, node: GameMoveNode) -> GameResult:
        if not self.no_moves_left(node):
            raise NotTerminalNodeError

    def pretty_print_node(self, node_key: int):
        state = self.__storage.get(node_key).moves

        print(f"""
            {state[0]} | {state[1]} | {state[2]}
           ---|---|---
            {state[3]} | {state[4]} | {state[5]}
           ---|---|---
            {state[6]} | {state[7]} | {state[8]}
        """)

    def init_root_node(self) -> GameMoveNode:
        node_key = hash(TicTacToeGameStrategy.__INITIAL_STATE)
        self.__storage.set(key=node_key, value=TicTacToeGameStrategy.__INITIAL_STATE)

        return GameMoveNode(key=node_key, parent=None)
