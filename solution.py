from player import Player
from board import HexBoard
import random


class SmartPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> tuple:
        """
        Decides the move using Minimax with Alpha-Beta pruning (depth 3).
        """
        possible_moves = self.get_possible_moves(board)
        if not possible_moves:
            return None

        # Start Minimax search
        best_move = None
        best_value = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for move in possible_moves:
            # Simulate move
            sim_board = board.clone()
            sim_board.place_piece(move[0], move[1], self.player_id)

            # Call minimax with alpha-beta parameters
            val = self.minimax(
                sim_board, depth=2, maximizing_player=False, alpha=alpha, beta=beta
            )

            if val > best_value:
                best_value = val
                best_move = move

            # Update alpha for the root level
            alpha = max(alpha, best_value)

        return best_move

    def minimax(
        self,
        board: HexBoard,
        depth: int,
        maximizing_player: bool,
        alpha: float,
        beta: float,
    ) -> float:
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
                eval = self.minimax(sim_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            opponent = 3 - self.player_id
            for move in possible_moves:
                sim_board = board.clone()
                sim_board.place_piece(move[0], move[1], opponent)
                eval = self.minimax(sim_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
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
