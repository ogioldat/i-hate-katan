from typing import Type
from lib.game import GameStrategy, GameMoveNode, ExplorationStatus
from debug.tree import pretty_print_tree
from .selection_policy import UCB1SelectionPolicy


class MaxExplorationDepthExceededError(Exception):
    def __init__(self, node: GameMoveNode, max_depth: int) -> None:
        self.message = f"Max depth {max_depth} exceeded!"
        super().__init__(self.message, node)


"""
Monte Carlo Tree Search consists of 4 steps:
1. Move (node) selection
2. Expansion
3. Simulation
4. Back-propagation
"""


class MonteCarloTreeSearch:
    def __init__(
        self,
        game_strategy: Type[GameStrategy],
        selection_policy: Type[UCB1SelectionPolicy] = UCB1SelectionPolicy(),
        simulations=int(1000),
        max_depth=int(10000),
    ) -> None:
        self.__simulations = simulations
        self.__game_strategy = game_strategy
        self.__selection_policy = selection_policy
        self.__max_depth = max_depth

    def run(self):
        root_node = self.__game_strategy.init_root_node()
        self.__game_strategy.expand_moves(root_node)

        explored_node = root_node

        for _ in range(self.__simulations):
            self.__simulate(explored_node)

        pretty_print_tree(root_node)

    def __simulate(self, node: GameMoveNode):
        depth = 0

        while True:
            node = self.__selection_policy.select(node)
            status = self.__game_strategy.exploration_status(node)

            if status.no_possible_moves:
                self.__backpropagate(node, status)
                break

            self.__game_strategy.expand_moves(node)

            depth += 1
            if depth > self.__max_depth:
                raise MaxExplorationDepthExceededError(self.__max_depth)

    def __backpropagate(self, node: GameMoveNode, status: ExplorationStatus):
        def populate_stats(node: GameMoveNode, is_winner: bool):
            node.visit()

            if is_winner:
                node.add_wins()

            if node.is_root():
                return

            populate_stats(node.parent, is_winner)

        is_winner = False
        if status.winner_node is not None:
            is_winner = True

        populate_stats(node, is_winner)
