from player import Player
from board import HexBoard
import random
import heapq


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
            return 10000.0
        opponent = 3 - self.player_id
        if board.check_connection(opponent):
            return -10000.0

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
        Dijkstra-based heuristic:
        Returns: opponent_distance - my_distance
        """
        my_dist = self.calculate_distance(board, self.player_id)
        opponent_id = 3 - self.player_id
        op_dist = self.calculate_distance(board, opponent_id)

        return op_dist - my_dist

    def calculate_distance(self, board: HexBoard, player_id: int) -> float:
        """
        Calculates the shortest path distance to connect the player's sides.
        Weights:
        - Own cell: 0
        - Empty cell: 1
        - Opponent cell: 100 (high cost but passable)
        """
        size = board.size
        # Priority Queue: (cost, r, c)
        pq = []
        # Min Distances Matrix initialized to infinity
        dists = [[float("inf") for _ in range(size)] for _ in range(size)]

        # Directions for neighbors
        directions = board.HEX_DIRECTIONS

        # Initialize PQ with starting edge cells
        if player_id == 1:  # Left to Right (Start at Col 0)
            for r in range(size):
                cost = self.get_cell_cost(board.board[r][0], player_id)
                dists[r][0] = cost
                heapq.heappush(pq, (cost, r, 0))
        else:  # Top to Bottom (Start at Row 0)
            for c in range(size):
                cost = self.get_cell_cost(board.board[0][c], player_id)
                dists[0][c] = cost
                heapq.heappush(pq, (cost, 0, c))

        while pq:
            current_cost, r, c = heapq.heappop(pq)

            # If we found a shorter path before, ignore
            if current_cost > dists[r][c]:
                continue

            # Check if we reached the target edge
            if player_id == 1 and c == size - 1:
                return current_cost
            if player_id == 2 and r == size - 1:
                return current_cost

            # Explore neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size:
                    move_cost = self.get_cell_cost(board.board[nr][nc], player_id)
                    new_cost = current_cost + move_cost
                    if new_cost < dists[nr][nc]:
                        dists[nr][nc] = new_cost
                        heapq.heappush(pq, (new_cost, nr, nc))

        return float("inf")

    def get_cell_cost(self, cell_value: int, player_id: int) -> int:
        if cell_value == player_id:
            return 0
        elif cell_value == 0:
            return 1
        else:
            return 100  # High cost for opponent cells

    def get_possible_moves(self, board: HexBoard):
        """Returns a list of all empty cells (r, c)"""
        moves = []
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] == 0:
                    moves.append((r, c))
        return moves
