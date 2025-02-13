from game import GameStrategy, GameResult, GameMoveNode, NotTerminalNodeError

class DummyGameStrategy(GameStrategy):
    def expand_moves(self, node: GameMoveNode) -> None:
        pass
    
    def no_moves_left(self, node: GameMoveNode) -> bool:
        return True 
    
    def random_game(self, node: GameMoveNode) -> GameResult:
        if not self.is_terminal_move(node):
            raise NotTerminalNodeError