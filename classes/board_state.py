import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900
}

VICTORY_VALUE = 25600

class BoardState:
    def __init__(self, board: chess.Board) -> None:
        self.board = board.copy(stack = True)

    def getLegalMovesWithSAN(self) -> list[tuple[chess.Move, str]]:
        legal_moves = self.board.legal_moves

        return_array = [
            (move, self.board.san(move))
            for move in legal_moves
        ]

        return return_array
    
    def getBoardStateAfterMove(self, move: chess.Move) -> BoardState:
        board_copy = self.board.copy(stack = True)

        board_copy.push(move)

        return BoardState(board_copy)

    def getBoardStateAfterMoveSAN(self, move_SAN: str) -> BoardState:
        move = self.board.parse_san(move_SAN)

        return self.getBoardStateAfterMove(move)

    # def isDraw(self) -> bool:
        # return self.board.is_insufficient_material() or self.board.is_stalemate() or self.board.is_fifty_moves() or self.board.can_claim_threefold_repetition()

    def getTotalPieceValueEvaluation(self, victory_value_offset: int) -> int:
        if self.board.outcome():            
            outcome = self.board.outcome()
            assert outcome

            # print("ran", outcome.termination)

            if outcome.winner == chess.WHITE:
                return VICTORY_VALUE + victory_value_offset
            elif outcome.winner == chess.BLACK:
                return -(VICTORY_VALUE + victory_value_offset)
            else:
                return 0
        
        total_piece_value_for_white = 0
        total_piece_value_for_black = 0

        for _, (piece_type, piece_value) in enumerate(PIECE_VALUES.items()):
            # print(index, piece_type)

            total_piece_value_for_white += piece_value * len(
                self.board.pieces(piece_type, chess.WHITE)
            )

            # print(total_piece_value_for_white)

            total_piece_value_for_black += piece_value * len(
                self.board.pieces(piece_type, chess.BLACK)
            )

            # print(total_piece_value_for_black)

        return total_piece_value_for_white - total_piece_value_for_black    
        
    def __str__(self):
        return self.board.__str__()

    
