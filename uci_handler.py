#!/usr/bin/env python3
import chess
import sys, threading

from classes.engine import Engine
from classes.board_state import BoardState

def find_best_move(board: chess.Board, time_on_clock_ms: int, increment_ms: int) -> str | None:
    try:
        maximum_time_per_move_to_not_flag = (time_on_clock_ms / 1000) / 15 + (increment_ms / 1000)

        if board.fullmove_number < 2:
            maximum_time_per_move_to_not_flag = 9

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

        depth = 4

        if maximum_time_per_move_to_not_flag > 0.217:
            depth = 4
        else:
            depth = 2

        current_board_state = BoardState(board)

        current_engine = Engine()

        # print(f"Using depth: {depth} as my_time is {time_on_clock_ms} ms and my_inc is {increment_ms} ms")
        
        move, _, _ = current_engine.pickNextMoveWithNextBoardStateEval(current_board_state, depth)

        return move.uci()

    except Exception as e:
        print(f"info string Engine error: {e}", file=sys.stderr)
        return None
# -----------------------------------

class UciWrapper:
    def __init__(self):
        self.board = chess.Board()
        self.running = True

        self.wtime = 0
        self.btime = 0

    def run(self):
        print("id name GalliumChessEngine")
        print("id author whatisenpassant1")

        print("option name MoveOverheadMs type spin default 10 min 0 max 5000")
        print("option name Threads type spin default 1 min 1 max 128")

        print("uciok")

        sys.stdout.flush()

        while self.running:
            try:
                line = sys.stdin.readline().strip()
                if not line:
                    continue
                self.process_command(line)
            except EOFError:
                break
            except ValueError:
                continue

    def process_command(self, line: str):
        """Parses and executes UCI commands."""
        parts = line.split()
        command = parts[0]

        if command == "uci":
            print("uciok")
        elif command == "isready":
            print("readyok")
            sys.stdout.flush()

        elif command == "quit":
            self.running = False
        elif command == "position":
            self.handle_position(parts[1:])
        elif command == "go":
            self.handle_go(parts[1:])
            sys.stdout.flush()

        elif command == "ucinewgame":
            self.board = chess.Board()

    def handle_position(self, args: list[str]):
        """Sets the board position from FEN or a sequence of moves."""
        if args[0] == "startpos":
            self.board = chess.Board()
            moves_index = 1
        elif args[0] == "fen":
            fen = " ".join(args[1:7])
            self.board = chess.Board(fen)
            moves_index = 7
        else:
            return

        if len(args) > moves_index and args[moves_index] == "moves":
            for move_uci in args[moves_index+1:]:
                move = chess.Move.from_uci(move_uci)
                if move in self.board.legal_moves:
                    self.board.push(move)

    def handle_go(self, args: list[str]):
        """Initiates the search for the best move."""
        # Parse time limits from the 'go' command arguments
        self.wtime, self.btime = (10000, 10000)
        self.winc, self.binc = (0, 0)

        try:
            for i in range(0, len(args), 2):
                if args[i] == "wtime":
                    self.wtime = int(args[i+1])
                elif args[i] == "btime":
                    self.btime = int(args[i+1])
                elif args[i] == "winc": 
                    self.winc = int(args[i+1])
                elif args[i] == "binc": 
                    self.binc = int(args[i+1])
                # We can also parse 'depth', 'movetime', 'nodes', etc.
        except (IndexError, ValueError):
            pass

        # Use the correct time based on whose turn it is
        if self.board.turn == chess.WHITE:
            time_left, inc = self.wtime, self.winc
        else:
            time_left, inc = self.btime, self.binc
        
        # Provide a default time limit if not specified (e.g., 1 second)
        if time_left == 0:
            time_left = 1000 

        # Start search in a separate thread so the script can still respond to 'stop'
        search_thread = threading.Thread(target=self.search_and_report, args = (time_left, inc))
        search_thread.start()

    def search_and_report(self, time_limit_ms: int, increment_ms: int):
        """Calls the actual engine logic and prints the result."""
        best_move_uci = find_best_move(self.board.copy(), time_limit_ms, increment_ms)
        if best_move_uci:
            print(f"bestmove {best_move_uci}")

            sys.stdout.flush()

if __name__ == "__main__":
    wrapper = UciWrapper()
    wrapper.run()
