import chess

import time, sys

from classes.board_state import BoardState
from classes.engine import Engine

currentBoardState: BoardState = BoardState(chess.Board())
currentEngine: Engine = Engine()

def makeUserChooseOption(options: set[str], message: str, retry_message: str):
    user_response = input(message)

    while True:
        if user_response in options:
            return user_response
        
        print(retry_message)

        user_response = input(message)

def playMoveAsBot():
    print("Thinking...")

    time.sleep(2)

    move, move_san = currentEngine.pickNextMove(currentBoardState)

    new_board_state = currentBoardState.getBoardStateAfterMove(move)

    print(new_board_state)

    print(f"I played {move_san}. The board evaluation is now {new_board_state.getTotalPieceValueEvaluation()}")

    return new_board_state

def handleGameOverState():
    outcome = currentBoardState.board.outcome()

    if outcome:
        print(f"Game Over!")
        print(f"Winner: {'White' if outcome.winner == chess.WHITE else ('Black' if outcome.winner == chess.BLACK else 'None (Draw)')}")      # True for White, False for Black, None for Draw
        print(f"Result: {outcome.result()}")    # "1-0", "0-1", or "1/2-1/2"
        print(f"Reason: {outcome.termination}") # e.g., Termination.CHECKMATE

        return True

def playMoveAsPlayer():
    while True:
        move_picked_by_user = input("Enter your move in SAN: ")

        try:
            new_board_state = currentBoardState.getBoardStateAfterMoveSAN(move_picked_by_user)

            break

        except ValueError:
            print("Illegal move, try again.")

    print(new_board_state)

    print(f"The board evaluation is now {new_board_state.getTotalPieceValueEvaluation()}.")

    return new_board_state

player_desired_colour = makeUserChooseOption(
    {"W", "B"},
    "Which colour do you want to start as? (W/B): ",
    "That is not a valid colour! Pick 'W' for White and 'B'za for Black."    
)

print(currentBoardState)

if player_desired_colour == "W":
    currentBoardState = playMoveAsPlayer()

while True:
    currentBoardState = playMoveAsBot()

    if handleGameOverState():
        input()

        sys.exit()

    currentBoardState = playMoveAsPlayer()

    if handleGameOverState():
        input()

        sys.exit()
