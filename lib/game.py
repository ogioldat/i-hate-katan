from abc import ABC as AbstractBaseClass, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Dict, Type

NodeKey = int


@dataclass
class GameMoveNodeScore:
    wins = 0
    visits = 0


@dataclass
class GameStateShape(AbstractBaseClass):
    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass


TGameStateShape = TypeVar("TGameStateShape", bound=GameStateShape)


class GameStateStorage(Generic[TGameStateShape]):
    def __init__(self, shape: Type[TGameStateShape]):
        self.__storage: Dict[NodeKey, shape] = dict()

    def set(self, key: NodeKey, value: TGameStateShape) -> None:
        self.__storage[key] = value

    def get(self, key: NodeKey) -> TGameStateShape:
        if key not in self.__storage:
            raise MissingStorageEntryError(key)

        return self.__storage.get(key)

    def has(self, key: NodeKey) -> bool:
        return key in self.__storage.keys()


class MissingStorageEntryError(Exception):
    def __init__(self, key: NodeKey) -> None:
        self.message = f'Missing "{key}" key!'
        super().__init__(self.message, key)


class GameMoveNode:
    def __init__(self, key: NodeKey, parent=None):
        self.__children: Dict[NodeKey, GameMoveNode] = dict()
        self.__parent = parent
        self.key = key
        self.__score = GameMoveNodeScore()

    def visit(self):
        self.__score.visits += 1

    def add_wins(self, num=int(1)):
        self.__score.wins += num

    def is_root(self) -> bool:
        return self.__parent is None

    @property
    def score(self) -> GameMoveNodeScore:
        return self.__score

    @property
    def parent(self):
        return self.__parent

    def child(self, key: NodeKey):
        if key not in self.__children:
            raise MissingChildNodeError(self, key=key)

        return self.__children.get(key)

    @property
    def children(self):
        return self.__children

    def append(self, key: NodeKey):
        new_node = GameMoveNode(parent=self, key=key)
        self.__children[key] = new_node

        return new_node

    def is_leaf_node(self) -> bool:
        return len(self.__children) == 0

    def __repr__(self) -> str:
        return f"key={self.key}"

    def __str__(self) -> str:
        return str(self.key)


class MissingChildNodeError(Exception):
    def __init__(self, node: GameMoveNode, key: int) -> None:
        self.message = f'Missing child node with "{key}" key!'
        super().__init__(self.message, node)


class NotTerminalNodeError(Exception):
    def __init__(self, node: GameMoveNode, key: int) -> None:
        self.message = f'Not terminal node with "{key}" key!'
        super().__init__(self.message, node)


@dataclass
class GameResult:
    score: int
    moves: int
    terminal_node: GameMoveNode


class GameStrategy(AbstractBaseClass):
    storage: GameStateStorage
    storage_shape: Type[TGameStateShape]

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

    def _create_state_storage(
        self, storage_shape: Type[TGameStateShape]
    ) -> GameStateStorage[TGameStateShape]:
        return GameStateStorage(shape=storage_shape)

    @abstractmethod
    def init_root_node() -> GameMoveNode:
        pass
