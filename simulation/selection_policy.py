from abc import ABC, abstractmethod
from math import log as ln, sqrt
from lib.game import GameMoveNode


class SelectionPolicy(ABC):
    @abstractmethod
    def select(node: GameMoveNode) -> GameMoveNode:
        pass


class FirstChildNodeSelectionPolicy(SelectionPolicy):
    def select(self, node: GameMoveNode) -> GameMoveNode:
        return next(iter(node.children.values()))


"""
    UCT stands for Upper Confidence Bound for Trees
    TODO: Explore alternatives UCB1-tuned
"""


class UCB1SelectionPolicy(SelectionPolicy):
    def __init__(self, exploration_const=sqrt(2)) -> None:
        super().__init__()
        self.__exploration_const = exploration_const

    def __ucb1_score(self, node: GameMoveNode) -> float:
        reward_visit_ratio = float(node.wins / node.visit)
        ucb1 = reward_visit_ratio + self.__exploration_const * sqrt(
            ln(node.parent.visit) / node.visits
        )

        return ucb1

    def select(self, node: GameMoveNode) -> GameMoveNode:
        max_score = (float("-inf"), GameMoveNode(key=0))

        for child_node in node.__children.values():
            score = self.__ucb1_score(child_node)

            if score > max_score[0]:
                max_score = (score, child_node)

        return max_score[1]
