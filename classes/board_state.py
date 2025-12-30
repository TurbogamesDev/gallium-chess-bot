import chess

class BoardState:
    def __init__(self, board: chess.Board):
        self.board: chess.Board = board

    def getLegalMoves(self):
        legal_moves = list(self.board.generate_legal_moves())

        return_array = []

        for move in legal_moves:
            return_array.append(
                (move, self.board.san(move))
            )
        
        return return_array
    
    def playMove(self, move):
        self.board.push(move)

    def playMoveSAN(self, move_SAN: str):
        move = self.board.parse_san(move_SAN)

        self.playMove(move)

    def __str__(self):
        return self.board.__str__()

    
