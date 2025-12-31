# Roadmap:
# 1. Implement depth-limited minimax with piece-value evaluation
# 2. Add alpha-beta pruning
# 3. Introduce slight leaf randomness (±0.1)
# 4. Candidate-focused fuzzing on last 2 plies
# 5. (Optional) Lichess integration

import chess

import random, time, sys

from classes.board_state import BoardState

current_board_state: BoardState = BoardState(chess.Board())

def playMoveAsBot():
    print("Thinking...")

    time.sleep(2)

    move, move_san = random.choice(
        current_board_state.getLegalMovesWithSAN()
    )

    new_board_state = current_board_state.playMove(move)

    print(new_board_state)

    print(f"I played {move_san}.")

    return new_board_state

def handleGameOverState():
    outcome = current_board_state.board.outcome()

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
            new_board_state = current_board_state.playMoveSAN(move_picked_by_user)

            break

        except ValueError:
            print("Illegal move, try again.")

    print(new_board_state)

    return new_board_state

player_desired_colour = ""

while True:
    player_desired_colour = input("Which colour do you want to start as? (W/B): ")

    if player_desired_colour in ["W", "B"]:
        break

print(current_board_state)

if player_desired_colour == "W":
    current_board_state = playMoveAsPlayer()

while True:
    current_board_state = playMoveAsBot()

    if handleGameOverState():
        sys.exit()

    current_board_state = playMoveAsPlayer()

    if handleGameOverState():
        sys.exit()


# while True:
    # legal_moves = board.generate_legal_moves()

    # move_to_pick = random.choice(list(legal_moves))

    # move_to_pick_in_SAN = board.san(move_to_pick)

    # board.push(move_to_pick)

    # print(board)
    # print(f"I played {move_to_pick_in_SAN}.")
    
    

    # print(board)

    # outcome = board.outcome()

    # if outcome:
    #     print(f"Game Over!")
    #     print(f"Winner: {"White" if outcome.winner else ("Black" if outcome.winner == False else "None (Draw)")}")      # True for White, False for Black, None for Draw
    #     print(f"Result: {outcome.result()}")    # "1-0", "0-1", or "1/2-1/2"
    #     print(f"Reason: {outcome.termination}") # e.g., Termination.CHECKMATE

    #     sys.exit()

    # print("Thinking...")

    # time.sleep(2)

