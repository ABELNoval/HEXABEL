from player import Player
from board import HexBoard
import time
import heapq


class SmartPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
        # Time control configuration
        self.max_time = 4.8  # Seconds (0.2s margin for the 5s limit)
        self.start_time = 0
        self.timeout = False

    def play(self, board: HexBoard) -> tuple:
        """
        Decides the move using Minimax with Iterative Deepening Alpha-Beta pruning.
        Includes Time Control, Move Reduction, and Ordering.
        """
        self.start_time = time.time()
        self.timeout = False

        # 1. Move Reduction (Get only relevant moves)
        possible_moves = self.get_relevant_moves(board)

        if not possible_moves:
            # Fallback: try all empty cells if no relevant moves found
            possible_moves = self.get_possible_moves(board)

        if not possible_moves:
            return None

        # 2. Initial Ordering (Simple Heuristic)
        # Order moves to improve Alpha-Beta pruning efficiency
        possible_moves = self.order_moves(board, possible_moves)

        best_move = possible_moves[0]

        # 3. Iterative Deepening (Progressive depth until time runs out)
        max_depth = 1

        while True:
            try:
                if self.check_timeout():
                    break

                # Search with current depth
                current_best_move, current_val = self.search_root(
                    board, max_depth, possible_moves
                )

                # Update best move if search completed
                best_move = current_best_move

                # Stop if max possible depth reached
                if max_depth >= board.size * board.size:
                    break

                max_depth += 1

            except TimeoutError:
                break

        return best_move

    def check_timeout(self):
        if time.time() - self.start_time > self.max_time:
            self.timeout = True
            return True
        return False

    def search_root(self, board: HexBoard, depth: int, ordered_moves: list):
        """Root of Minimax to handle the returned move"""
        best_val = float("-inf")
        best_move = ordered_moves[0]
        alpha = float("-inf")
        beta = float("inf")

        for move in ordered_moves:
            if self.check_timeout():
                raise TimeoutError()

            sim_board = board.clone()
            sim_board.place_piece(move[0], move[1], self.player_id)

            # Call minimax with reduced depth
            val = self.minimax(sim_board, depth - 1, False, alpha, beta)

            if val > best_val:
                best_val = val
                best_move = move

            alpha = max(alpha, best_val)

        return best_move, best_val

    def minimax(
        self,
        board: HexBoard,
        depth: int,
        maximizing_player: bool,
        alpha: float,
        beta: float,
    ) -> float:

        if self.check_timeout():
            raise TimeoutError()

        # Check terminal states
        if board.check_connection(self.player_id):
            return 10000.0
        opponent = 3 - self.player_id
        if board.check_connection(opponent):
            return -10000.0

        if depth == 0:
            return self.evaluate_board(board)

        # Generate relevant moves for this state
        moves = self.get_relevant_moves(board)
        if not moves:
            # Fallback to all possible moves if local search fails
            moves = self.get_possible_moves(board)
            if not moves:
                return self.evaluate_board(board)

        # Order moves (optional here, might be too costly)
        # moves = self.order_moves(board, moves)

        if maximizing_player:
            max_eval = float("-inf")
            for move in moves:
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
            for move in moves:
                sim_board = board.clone()
                sim_board.place_piece(move[0], move[1], opponent)
                eval = self.minimax(sim_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_relevant_moves(self, board: HexBoard):
        """
        Move Reduction Strategy.
        Considers only empty neighbors of existing pieces (distance 1).
        If board is empty, returns the center.
        """
        occupied = []
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] != 0:
                    occupied.append((r, c))

        if not occupied:
            return [(board.size // 2, board.size // 2)]

        relevant = set()
        for r, c in occupied:
            for dr, dc in board.HEX_DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.size and 0 <= nc < board.size:
                    if board.board[nr][nc] == 0:
                        relevant.add((nr, nc))

        # Convert to list
        moves = list(relevant)

        # Fallback: If no adjacent moves, return all possible moves
        if not moves:
            return self.get_possible_moves(board)

        return moves

    def order_moves(self, board: HexBoard, moves: list):
        """
        Move Ordering Strategy.
        Simple heuristic:
        1. Number of allied neighbors (connectivity).
        2. Proximity to center.
        """
        center = board.size // 2

        def quick_score(move):
            r, c = move
            # Distance to center
            dist_center = abs(r - center) + abs(c - center)

            # Allied neighbors
            my_neighbors = 0
            for dr, dc in board.HEX_DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.size and 0 <= nc < board.size:
                    if board.board[nr][nc] == self.player_id:
                        my_neighbors += 1

            # Score: High weight for neighbors, slight penalty for distance
            return (my_neighbors * 10) - dist_center

        return sorted(moves, key=quick_score, reverse=True)

    def get_possible_moves(self, board: HexBoard):
        """Returns all empty cells (fallback)"""
        moves = []
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] == 0:
                    moves.append((r, c))
        return moves

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
