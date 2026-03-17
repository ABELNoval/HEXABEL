from player import Player
from board import HexBoard
import random


class SmartPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> tuple:
        """
        Decides the move using Minimax with depth 3.
        """
        possible_moves = self.get_possible_moves(board)
        if not possible_moves:
            return None

        # Start Minimax search
        best_move = None
        best_value = float("-inf")

        # Depth 3: Current move (max) -> Opponent (min) -> Me (max) -> Evaluate
        # We call minimax with depth=2 beacuse the current loop is the first level.
        for move in possible_moves:
            # Simulate move
            sim_board = board.clone()
            sim_board.place_piece(move[0], move[1], self.player_id)

            # Call minimax for the opponent (minimizing step)
            val = self.minimax(sim_board, depth=2, maximizing_player=False)

            if val > best_value:
                best_value = val
                best_move = move

        return best_move

    def minimax(self, board: HexBoard, depth: int, maximizing_player: bool) -> float:
        # Check terminal states (Win/Loss)
        if board.check_connection(self.player_id):
            return 1000.0
        opponent = 3 - self.player_id
        if board.check_connection(opponent):
            return -1000.0

        # If max depth reached or no moves left, evaluate heuristically
        if depth == 0 or not self.get_possible_moves(board):
            return self.evaluate_board(board)

        possible_moves = self.get_possible_moves(board)

        if maximizing_player:
            max_eval = float("-inf")
            for move in possible_moves:
                sim_board = board.clone()
                sim_board.place_piece(move[0], move[1], self.player_id)
                eval = self.minimax(sim_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            opponent = 3 - self.player_id
            for move in possible_moves:
                sim_board = board.clone()
                sim_board.place_piece(move[0], move[1], opponent)
                eval = self.minimax(sim_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self, board: HexBoard) -> float:
        """
        Basic heuristic to evaluate board state.
        Strategy: Centrality.
        """
        score = random.uniform(0, 0.1)  # Small random factor to break ties
        center = board.size // 2

        for r in range(board.size):
            for c in range(board.size):
                cell = board.board[r][c]
                if cell == 0:
                    continue

                # Value proximity to center
                dist = abs(r - center) + abs(c - center)
                val = max(1, board.size - dist)

                if cell == self.player_id:
                    score += val
                else:
                    score -= val  # Subtract points for opponent positions

        return score

    def get_possible_moves(self, board: HexBoard):
        """Returns a list of all empty cells (r, c)"""
        moves = []
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] == 0:
                    moves.append((r, c))
        return moves
