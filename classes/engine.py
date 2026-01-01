import chess
import random

from classes.board_state import BoardState

LARGE_INT: int = 2 ** 24

VICTORY_VALUE_OFFSET = 10

class Engine:
    def __init__(self) -> None:
        pass
    
    def getBestMoveByMinimax(self, board_state: BoardState, depth: int, maximizing_player: bool, pruning: bool, alpha: int, beta: int) -> tuple[list[chess.Move], int]:
        # if board_state.board.outcome():
            # print(board_state.board.outcome()) 
        
        if depth == 0 or board_state.board.outcome():
            return ([], board_state.getTotalPieceValueEvaluation(VICTORY_VALUE_OFFSET * depth))
        
        if maximizing_player:
            moves_with_max_eval: list[chess.Move] = [] 
            max_eval: int = -LARGE_INT

            for move in board_state.getLegalMoves():
                new_board_state = board_state.getBoardStateAfterMove(move)

                _, eval = self.getBestMoveByMinimax(new_board_state, depth - 1, False, pruning, alpha, beta)
                
                if eval == max_eval:
                    moves_with_max_eval.append(move)
                elif eval > max_eval:
                    max_eval = eval
                    moves_with_max_eval = [move]

                if not pruning:
                    continue
                
                alpha = max(alpha, eval)

                if alpha > beta:
                    # print(alpha, beta)

                    break

            return (moves_with_max_eval, max_eval)
        
        else:
            moves_with_min_eval: list[chess.Move] = [] 
            min_eval: int = LARGE_INT

            for move in board_state.getLegalMoves():
                new_board_state = board_state.getBoardStateAfterMove(move)

                _, eval = self.getBestMoveByMinimax(new_board_state, depth - 1, True, pruning, alpha, beta)

                if eval == min_eval:
                    moves_with_min_eval.append(move)
                elif eval < min_eval:
                    min_eval = eval
                    moves_with_min_eval = [move]

                if not pruning:
                    continue
                
                beta = min(beta, eval)

                if alpha > beta:
                    break

            return (moves_with_min_eval, min_eval)

            # min_eval: int = LARGE_INT

            # for (move, _) in board_state.getLegalMovesWithSAN():
            #     new_board_state = board_state.getBoardStateAfterMove(move)

            #     eval = self.getBestMoveByMinimax(new_board_state, depth - 1, True)

            #     min_eval = min(min_eval, eval)

            # return min_eval

    def pickNextMoveWithNextBoardStateEval(self, board_state: BoardState, depth: int) -> tuple[chess.Move, str, int]:
        best_moves: list[chess.Move]
        best_moves_eval: int

        best_moves, best_moves_eval = self.getBestMoveByMinimax(
            board_state, 
            depth, 
            True if board_state.board.turn == chess.WHITE else False,
            True,
            -LARGE_INT,
            LARGE_INT
        )

        # unpruned_best_moves, unpruned_best_moves_eval = self.getBestMoveByMinimax(
        #     board_state, 
        #     depth, 
        #     True if board_state.board.turn == chess.WHITE else False,
        #     False,
        #     -LARGE_INT,
        #     LARGE_INT
        # )

        # print(best_moves == unpruned_best_moves)

        # print(best_moves_eval - unpruned_best_moves_eval)

        # print(best_moves_eval, best_moves)

        chosen_move = random.choice(best_moves)

        return (
            chosen_move,
            board_state.board.san(chosen_move),
            best_moves_eval
        )
