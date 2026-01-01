import chess
import random

from classes.board_state import BoardState

LARGE_INT: int = 2 ** 24

VICTORY_VALUE_OFFSET = 10

class Engine:
    def __init__(self) -> None:
        pass
    
    def getBestMoveByMinimax(self, board_state: BoardState, depth: int, maximizing_player: bool, pruning: bool, alpha: int, beta: int, topmost_node: bool) -> tuple[list[chess.Move], int]:
        # if board_state.board.outcome():
            # print(board_state.board.outcome()) 
        
        if depth == 0 or board_state.board.outcome():
            return ([], board_state.getTotalPieceValueEvaluation(VICTORY_VALUE_OFFSET * depth))
        
        if maximizing_player:
            moves_with_max_eval: list[chess.Move] = [] 
            max_eval: int = -LARGE_INT

            for move in board_state.getLegalMoves(depth > 1, depth == 1 and not topmost_node):
                # new_board_state = board_state.getBoardStateAfterMove(move)

                board_state.applyMove(move)

                _, eval = self.getBestMoveByMinimax(board_state, depth - 1, not maximizing_player, pruning, alpha, beta, False)
                
                board_state.undoLastMove()

                if not topmost_node:
                    pass
                elif eval == max_eval:
                    moves_with_max_eval.append(move)
                elif eval > max_eval:
                    moves_with_max_eval = [move]

                max_eval = max(eval, max_eval)

                if not pruning:
                    continue
                
                alpha = max(alpha, eval)

                if alpha >= beta:
                    # print(alpha, beta)

                    break
            
            # if len(moves_with_max_eval) == 0 and topmost_node:
            #     print("moves with max eval empty despite being topmost note") 
            #     time.sleep(1)

            if max_eval == -LARGE_INT:
                max_eval = board_state.getTotalPieceValueEvaluation(0)

            return (moves_with_max_eval, max_eval)
        
        else:
            moves_with_min_eval: list[chess.Move] = [] 
            min_eval: int = LARGE_INT

            for move in board_state.getLegalMoves(depth > 1, depth == 1 and not topmost_node):
                # new_board_state = board_state.getBoardStateAfterMove(move)

                board_state.applyMove(move)

                _, eval = self.getBestMoveByMinimax(board_state, depth - 1, not maximizing_player, pruning, alpha, beta, False)
                
                board_state.undoLastMove()

                if not topmost_node:
                    pass
                elif eval == min_eval:
                    moves_with_min_eval.append(move)
                elif eval < min_eval:
                    moves_with_min_eval = [move]

                min_eval = min(eval, min_eval)

                if not pruning:
                    continue
                
                beta = min(beta, eval)

                if alpha >= beta:
                    break
            
            # if len(moves_with_min_eval) == 0 and topmost_node:
            #     print("moves with min eval empty despite being topmost note") 
            #     time.sleep(1)

            if min_eval == LARGE_INT:
                min_eval = board_state.getTotalPieceValueEvaluation(0)

            # print(moves_with_min_eval, min_eval)

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
            LARGE_INT,
            True
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
        try:
            chosen_move = random.choice(best_moves)
        except:
            print(f"No good moves found! Trying again with a lower depth ({depth - 1}). Evaluation was {best_moves_eval}")

            if depth == 1:
                print("Depth is already 1 so it cant be lowered. Picking a random move... ")

                # time.sleep(1)

                move = random.choice(
                        board_state.getLegalMoves(False, False)
                )

                return (
                    move,
                    board_state.board.san(move),
                    best_moves_eval
                )

            # time.sleep(1)

            return self.pickNextMoveWithNextBoardStateEval(board_state, depth - 1)

        return (
            chosen_move,
            board_state.board.san(chosen_move),
            best_moves_eval
        )
