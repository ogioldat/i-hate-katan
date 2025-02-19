from math import log as ln, sqrt
from typing import Type
from lib.game import GameStrategy, GameMoveNode, NotTerminalNodeError
from debug.tree import pretty_print_tree


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
        exploration_const=sqrt(2),
        simulations=int(1000),
        max_depth=int(10000),
    ) -> None:
        self.__exploration_const = exploration_const
        self.__simulations = simulations
        self.__game_strategy = game_strategy
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
            node = self.__select_move(node)
            if self.__game_strategy.no_moves_left(node):
                break

            self.__game_strategy.expand_moves(node)

            depth += 1
            if depth > self.__max_depth:
                raise MaxExplorationDepthExceededError(self.__max_depth)

    def __backpropagate(self, node: GameMoveNode):
        if not node.is_leaf_node():
            raise NotTerminalNodeError

    def __select_move(self, node: GameMoveNode) -> GameMoveNode:
        return next(iter(node.children.values()))
        # max_score = (0, GameMoveNode("empty"))

        # for child_node in node.__children.values():
        #     score = self.__selection_policy_score(child_node)

        #     if score > max_score[0]:
        #         max_score = (score, child_node)

        # return max_score[1]

    def __selection_policy_score(self, node: GameMoveNode) -> float:
        return self.__ucb1_score(node)

    """
    UCT stands for Upper Confidence Bound for Trees
    TODO: Explore alternatives UCB1-tuned
    """

    def __ucb1_score(self, node: GameMoveNode) -> float:
        reward_visit_ratio = float(node.wins / node.visit)
        ucb1 = reward_visit_ratio + self.__exploration_const * sqrt(
            ln(node.parent.visit) / node.visits
        )

        return ucb1
