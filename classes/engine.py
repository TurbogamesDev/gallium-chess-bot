import chess
import random

from .board_state import BoardState

class Engine:
    def __init__(self) -> None:
        pass
    
    def pickNextMove(self, board_state: BoardState) -> tuple[chess.Move, str]:
        move, move_san = random.choice(
            board_state.getLegalMovesWithSAN()
        )

        return (move, move_san)

    