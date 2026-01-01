import chess, chess.pgn

import sys, os, time

from classes.board_state import BoardState
from classes.engine import Engine

DEPTH = 5
# Average performance at different depths:
# 1: 0.96 ms
# 2: 2.62 ms
# 3: 19.65 ms
# 4: 106 ms
# 5: 10 0.5795950399944558 50 2.501087801987305 100 2.224732396993786
## Moves 1-5: 580 ms
## Moves 6-25: 2.98 s
## Moves 26+: 1.95 s
# 6: 10 3.358114630007185 50 5.118703947998584 100 4.44893065699609
## Moves 1-5: 3.36 s
## Moves 6-25: 5.56 s
## Moves 26+: 3.78 s

total_time: float = 0
no_of_searches: int = 0

currentBoardState: BoardState = BoardState(chess.Board())
currentEngine: Engine = Engine()

def makeUserChooseOption(options: set[str], message: str, retry_message: str):
    user_response = input(message)

    while True:
        if user_response in options:
            return user_response
        
        print(retry_message)

        user_response = input(message)

def clearTerminal():
    # return
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def playMoveAsBot():
    print("Thinking...")

    start_time = time.perf_counter()

    move, move_san, _ = currentEngine.pickNextMoveWithNextBoardStateEval(currentBoardState, DEPTH)

    end_time = time.perf_counter()

    new_board_state = currentBoardState.getBoardStateAfterMove(move)
    
    time_taken = end_time - start_time

    # best_moves, _ = currentEngine.getBestMoveByMinimax(new_board_state, DEPTH, True if new_board_state.board.turn == chess.WHITE else False)
    
    clearTerminal()

    print(new_board_state)

    print(f"I played {move_san}, which took me {str(round(time_taken * 1000)) + " ms" if time_taken < 1 else str(round(time_taken, 1)) + " s"} to calculate.")
    
    # global total_time
    # global no_of_searches

    # total_time += (end_time - start_time)
    # no_of_searches += 1
    
    # print(no_of_searches, total_time / no_of_searches)

    return new_board_state

def getPGN(board_state: BoardState) -> str:
    game = chess.pgn.Game.from_board(currentBoardState.board)
    exporter = chess.pgn.StringExporter(columns=None, headers=True, comments=True)
    pgn_string = game.accept(exporter)

    return pgn_string

def handleGameOverState():
    outcome = currentBoardState.board.outcome()

    if outcome:
        print(f"Game Over!")
        print(f"Winner: {'White' if outcome.winner == chess.WHITE else ('Black' if outcome.winner == chess.BLACK else 'None (Draw)')}")      # True for White, False for Black, None for Draw
        print(f"Result: {outcome.result()}")    # "1-0", "0-1", or "1/2-1/2"
        print(f"Reason: {outcome.termination}") # e.g., Termination.CHECKMATE

        print("PGN: ")
        print(getPGN(currentBoardState))

        return True

def playMoveAsPlayer():
    while True:
        move_picked_by_user = input("Enter your move in SAN, or type 'END' to end the game and get the PGN: ")

        # start_time = time.perf_counter()

        # _, move_san, _ = currentEngine.pickNextMoveWithNextBoardStateEval(currentBoardState, DEPTH)

        # end_time = time.perf_counter()

        # move_picked_by_user = move_san

        # print(move_san)

        # global total_time
        # global no_of_searches

        # total_time += (end_time - start_time)
        # no_of_searches += 1
        
        # print(no_of_searches, total_time / no_of_searches)

        # time.sleep(1.5)

        if move_picked_by_user == "END":
            print(getPGN(currentBoardState))

            input()

            sys.exit()

        try:
            new_board_state = currentBoardState.getBoardStateAfterMoveSAN(move_picked_by_user)

            break

        except ValueError:
            print("Illegal move, try again.")

    clearTerminal()

    print(new_board_state)

    # _, new_eval = currentEngine.getBestMoveByMinimax(new_board_state, DEPTH, True if new_board_state.board.turn == chess.WHITE else False)

    # print(f"The board evaluation is now {new_eval}.")

    return new_board_state

player_desired_colour = makeUserChooseOption(
    {"W", "B"},
    "Which colour do you want to start as? (W/B): ",
    "That is not a valid colour! Pick 'W' for White and 'B' for Black."    
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
