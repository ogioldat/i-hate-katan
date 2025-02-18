from abc import ABC as AbstractBaseClass, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Dict, Type

NodeKey = int


@dataclass
class GameMoveNodeScore:
    wins = 0
    visits = 0


@dataclass
class GameStateShape:
    pass


TGameStateShape = TypeVar("TGameStateShape", bound=GameStateShape)


class GameStateStorage(Generic[TGameStateShape]):
    def __init__(self, shape: Type[TGameStateShape]):
        self.__storage: Dict[NodeKey, shape] = dict()

    def set(self, key: NodeKey, value: TGameStateShape) -> None:
        self.__storage[key] = value

    def get(self, key: NodeKey) -> TGameStateShape:
        return self.__storage.get(key)

    def has(self, key: NodeKey) -> bool:
        return key in self.__storage.keys()


class GameMoveNode:
    def __init__(self, key: int, parent=None):
        self.children = GameMoveChildNodes()
        self.__parent = parent
        self.key = key
        self.__score = GameMoveNodeScore()

    def visit(self):
        self.__score.visits += 1

    def add_wins(self, num=int(0)):
        self.__score.wins += num

    def is_root(self) -> bool:
        return self.__parent is None

    @property
    def score(self) -> GameMoveNodeScore:
        return self.__score

    @property
    def parent(self):
        return self.__parent

    def append(self, key: int):
        new_node = GameMoveNode(parent=self, key=key)
        self.children[key] = new_node

    def is_leaf_node(self) -> bool:
        return len(self.children) == 0

    def __repr__(self) -> str:
        return f"key={self.key}"


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
    storage: GameStateStorage

    def __init__(self):
        self.__key_seq = 1

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

    def create_state_storage(
        self, storage_shape: Type[TGameStateShape]
    ) -> GameStateStorage[TGameStateShape]:
        return GameStateStorage(shape=storage_shape)

    def next_key(self) -> NodeKey:
        self.__key_seq += 1
        return self.__key_seq
