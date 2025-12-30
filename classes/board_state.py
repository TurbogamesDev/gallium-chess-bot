import chess

class BoardState:
    def __init__(self, board: chess.Board) -> None:
        self.board = board.copy(stack = False)

    def getLegalMovesWithSAN(self) -> list[tuple[chess.Move, str]]:
        legal_moves = self.board.legal_moves

        return_array = [
            (move, self.board.san(move))
            for move in legal_moves
        ]

        return return_array
    
    def playMove(self, move: chess.Move) -> BoardState:
        board_copy = self.board.copy(stack = False)

        board_copy.push(move)

        return BoardState(board_copy)

    def playMoveSAN(self, move_SAN: str) -> BoardState:
        move = self.board.parse_san(move_SAN)

        return self.playMove(move)

    def __str__(self):
        return self.board.__str__()

    
