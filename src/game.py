from abc import ABC as AbstractBaseClass, abstractmethod
from dataclasses import dataclass
from game import GameMoveNode

from random import randint
from dataclasses import dataclass

@dataclass
class GameMoveNodeScore:
    wins = 0
    visits = 0

class GameMoveNode:
    def __init__(self, label, parent = None, key = randint(1, 100000)):
        self.children = GameMoveChildNodes()
        self.__label = label
        self.__parent = parent
        self.key = key
        self.__score = GameMoveNodeScore()
        
    def visit(self):
        self.__score.visits += 1
        
    def add_wins(self, num = int(0)):
        self.__score.wins += num
    
    @property
    def score(self) -> GameMoveNodeScore:
        return self.__score
    
    def append(self, key, label) -> GameMoveNode:
        new_node = GameMoveNode(label=label, parent=self, key=key)
        self.children[key] = new_node
        
        return new_node 

    def is_leaf_node(self) -> bool:
        return len(self.children) == 0

class MissingChildNodeError(Exception):
    def __init__(self, node: GameMoveNode, key: int) -> None:
        self.message = f'Missing child node with "{key}" key!'
        super().__init__(self.message, node)
        
class NotTerminalNodeError(Exception):
    def __init__(self, node: GameMoveNode, key: int) -> None:
        self.message = f'Not terminal node with "{key}" key!'
        super().__init__(self.message, node)

class GameMoveChildNodes(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def __getitem__(self, key):
        if key in self.__children:
            return self.__children[key]
        
        raise MissingChildNodeError(self, key=key)

@dataclass
class GameResult:
    score: int
    moves: int
    terminal_node: GameMoveNode
    
class GameStrategy(AbstractBaseClass):
    @abstractmethod
    def expand_moves(self, node: GameMoveNode) -> None:
        pass
    
    @abstractmethod
    def no_moves_left(self, node: GameMoveNode) -> bool:
        pass
    
    @abstractmethod
    def random_game(self, node: GameMoveNode) -> GameResult:
        if not self.is_terminal_move(node):
            raise NotTerminalNodeError
        