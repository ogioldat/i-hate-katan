from lib.game import GameResult, GameStrategy, GameMoveNode


class CatanGameStrategy(GameStrategy):
    def expand_moves(self, node: GameMoveNode) -> None:
        return

    def no_moves_left(self, node: GameMoveNode) -> bool:
        return True

    def random_game(self, node: GameMoveNode) -> GameResult:
        return super().random_game(node)
