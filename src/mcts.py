from math import log as ln, sqrt
from abc import ABC as AbstractBaseClass, abstractmethod
from typing import Type
from random import randint

class ChildNodes(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def __getitem__(self, key):
        if key in self.__children:
            return self.__children[key]
        
        raise MissingChildNodeError(self, key=key)

class Node:
    def __init__(self, label, parent = None, key = randint(1, 100000)):
        self.children = ChildNodes()
        self.__visits = int(0)
        self.__wins = int(0)
        self.__label = label
        self.__parent = parent
        self.key = key
        
    def visit():
        __visits += 1
        
    def add_wins(self, num = int(0)):
        self.__wins += 1
    
    @property
    def visits(self) -> int:
        return self.__visits
    
    @property
    def wins(self) -> int:
        return self.__wins

    def append(self, child_node) -> None:
        self.children[child_node.key] = child_node

    def is_leaf_node(self) -> bool:
        return len(self.children) == 0


class MissingChildNodeError(Exception):
    def __init__(self, node: Node, key: int) -> None:
        self.message = f'Missing child node with "{key}" key!'
        super().__init__(self.message, node)
        
class NotTerminalNodeError(Exception):
    def __init__(self, node: Node, key: int) -> None:
        self.message = f'Not terminal node with "{key}" key!'
        super().__init__(self.message, node)
        
class GameStrategy(AbstractBaseClass):
    @abstractmethod
    def expand_possible_moves(self, node: Node) -> None:
        pass
    
    @abstractmethod
    def is_terminal_move(self, node: Node) -> bool:
        pass
    
    @abstractmethod
    def simulate(self, node: Node) -> None:
        if not self.is_terminal_move(node):
            raise NotTerminalNodeError

"""
Monte Carlo Tree Search consists of 4 steps:
1. Move (node) selection
2. Expansion
3. Simulation
4. Back-propagation
"""
class MonteCarloTreeSearch():
    def __init__(
        self,
        game_strategy: Type[GameStrategy],
        exploration_const = sqrt(2),
        simulations = int(1000) 
        ) -> None:
        self.__exploration_const = exploration_const
        self.__game_strategy = game_strategy()
        self.__root_node = Node(label="MCTS root")
    
    def run(self):
        root = self.__game_strategy.expand_possible_moves(self.__root_node)
        selected_node = self.select(root)
        
        while self.__game_strategy.is_terminal_move(selected_node):
            expanded_node = self.expand(selected_node)
            selected_node = self.select(expanded_node)
            
        self.__game_strategy.simulate(selected_node)
        
        
    def expand(self, node: Node) -> Node:
        self.__game_strategy.expand_possible_moves(node)
        return node
    
    def select(self, node: Node) -> Node:
        max_ucb = (0, Node("empty"))
        
        for child_node in node.children.values():
            ucb_score = self.__ucb1_score(child_node)
            
            if ucb_score > max_ucb[0]:
                max_ucb = (ucb_score, child_node)
                
        return max_ucb[1]
            

    """
    UCT stands for Upper Confidence Bound for Trees
    """
    def __ucb1_score(self, node: Node) -> Node:
        reward_visit_ratio = (node.wins / node.visit)
        ucb1 = reward_visit_ratio + self.__exploration_const * sqrt(
            ln(node.parent.visit) / node.visits
        )
        
        return ucb1
        
