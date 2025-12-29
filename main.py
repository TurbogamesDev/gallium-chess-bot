import chess, random, time, sys

board = chess.Board()

while True:
    legal_moves = board.generate_legal_moves()

    move_to_pick = random.choice(list(legal_moves))

    move_to_pick_in_SAN = board.san(move_to_pick)

    board.push(move_to_pick)

    print(board)
    print(f"I played {move_to_pick_in_SAN}.")

    outcome = board.outcome()

    if outcome:
        print(f"Game Over!")
        print(f"Winner: {"White" if outcome.winner else ("Black" if outcome.winner == False else "None (Draw)")}")      # True for White, False for Black, None for Draw
        print(f"Result: {outcome.result()}")    # "1-0", "0-1", or "1/2-1/2"
        print(f"Reason: {outcome.termination}") # e.g., Termination.CHECKMATE

        sys.exit()
    
    while True:
        move_picked_by_user = input("Enter your move in SAN: ")

        try:
            board.push_san(move_picked_by_user)

            break
        except ValueError:
            print("Illegal move, try again.")

    print(board)

    outcome = board.outcome()

    if outcome:
        print(f"Game Over!")
        print(f"Winner: {"White" if outcome.winner else ("Black" if outcome.winner == False else "None (Draw)")}")      # True for White, False for Black, None for Draw
        print(f"Result: {outcome.result()}")    # "1-0", "0-1", or "1/2-1/2"
        print(f"Reason: {outcome.termination}") # e.g., Termination.CHECKMATE

        sys.exit()

    print("Thinking...")

    time.sleep(2)

