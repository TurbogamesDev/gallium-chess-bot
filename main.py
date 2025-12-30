import chess

import random, time, sys

board = chess.Board()

def playMoveAsBot():
    print("Thinking...")

    time.sleep(2)

    move = random.choice(
        list(
            board.generate_legal_moves()
        )
    )

    move_SAN = board.san(move)

    board.push(move)

    print(board)

    print(f"I played {move_SAN}.")

def handleGameOverState():
    outcome = board.outcome()

    if outcome:
        print(f"Game Over!")
        print(f"Winner: {"White" if outcome.winner else ("Black" if outcome.winner == False else "None (Draw)")}")      # True for White, False for Black, None for Draw
        print(f"Result: {outcome.result()}")    # "1-0", "0-1", or "1/2-1/2"
        print(f"Reason: {outcome.termination}") # e.g., Termination.CHECKMATE

        return True

def playMoveAsPlayer():
    while True:
        move_picked_by_user = input("Enter your move in SAN: ")

        try:
            board.push_san(move_picked_by_user)

            break

        except ValueError:
            print("Illegal move, try again.")

    print(board)

player_desired_colour = ""

while True:
    player_desired_colour = input("Which colour do you want to start as? (W/B): ")

    if player_desired_colour in ["W", "B"]:
        break

print(board)

if player_desired_colour == "W":
    playMoveAsPlayer()

while True:
    playMoveAsBot()

    if handleGameOverState():
        sys.exit()

    playMoveAsPlayer()

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

