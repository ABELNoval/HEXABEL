from player import Player
from board import HexBoard
import time
import heapq


class SmartPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.max_time = 4.8
        self.start_time = 0
        self.timeout = False
        self.transposition_table = {}  # TT: Stores board analysis to prune search tree
        self.killer_moves = [
            [None] * 2 for _ in range(100)
        ]  # Killer Moves: [depth][slot]

    def play(self, board: HexBoard) -> tuple:
        """
        Executes the game strategy using Minimax with Iterative Deepening,
        Alpha-Beta Pruning, Transposition Tables, and strategic Move Ordering.
        """
        self.start_time = time.time()
        self.timeout = False

        # Reset TT for each turn to avoid memory overflow in long matches
        # and to clear stale positions from previous game stages
        self.transposition_table.clear()

        # Reset Killer Moves
        self.killer_moves = [[None] * 2 for _ in range(100)]

        # Opening Move Optimization
        if self.is_board_empty(board):
            return (board.size // 2, board.size // 2)

        # Check for immediate winning move first (highest priority)
        winning_move = self.find_immediate_win(board, self.player_id)
        if winning_move:
            return winning_move

        # Check if we must block an immediate opponent win
        opponent_id = 3 - self.player_id
        blocking_move = self.find_immediate_win(board, opponent_id)
        if blocking_move:
            return blocking_move

        # --- Move Generation & Reduction ---
        possible_moves = self.get_relevant_moves(board)

        if not possible_moves:
            return None

        # --- Move Ordering ---
        possible_moves = self.order_moves(board, possible_moves)

        best_move = possible_moves[0]

        # --- Iterative Deepening Search ---
        max_depth = 1
        search_board = (
            board.clone()
        )  # Clone once for search to allow in-place modification

        while True:
            try:
                if self.check_timeout():
                    break

                current_best_move, current_val = self.search_root(
                    search_board, max_depth, possible_moves
                )

                best_move = current_best_move

                # --- Early Termination ---
                # If a forced win is detected (high score), terminate search early.
                if current_val >= 9000.0:
                    break

                if max_depth >= board.size * board.size:
                    break

                max_depth += 1

            except TimeoutError:
                break

        return best_move

    def find_immediate_win(self, board: HexBoard, player_id: int):
        """Checks if placing a piece in any valid spot creates a connection."""
        empty_cells = []
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] == 0:
                    empty_cells.append((r, c))

        for r, c in empty_cells:
            board.board[r][c] = player_id
            if board.check_connection(player_id):
                board.board[r][c] = 0  # Undo
                return (r, c)
            board.board[r][c] = 0  # Undo

        return None

    def check_timeout(self):
        if time.time() - self.start_time > self.max_time:
            self.timeout = True
            return True
        return False

    def search_root(self, board: HexBoard, depth: int, ordered_moves: list):
        best_val = float("-inf")
        best_move = ordered_moves[0]
        alpha = float("-inf")
        beta = float("inf")

        for move in ordered_moves:
            if self.check_timeout():
                raise TimeoutError()

            # Apply move (Backtracking)
            board.board[move[0]][move[1]] = self.player_id

            try:
                val = self.minimax(board, depth - 1, False, alpha, beta)
            except TimeoutError:
                # Ensure we undo even on timeout if caught here,
                # though usually timeout propagates.
                # But to be safe for state consistency:
                board.board[move[0]][move[1]] = 0
                raise

            board.board[move[0]][move[1]] = 0  # Undo

            if val > best_val:
                best_val = val
                best_move = move

            # --- EARLY PRUNING AT ROOT ---
            # If we find a winning move at root (depth 1 of this iteration), take it.
            if val >= 9000.0:
                return move, val

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

        # --- Transposition Table Lookup ---
        board_hash = self.get_board_hash(board, maximizing_player)
        if board_hash in self.transposition_table:
            t_depth, t_flag, t_val = self.transposition_table[board_hash]
            if t_depth >= depth:
                if t_flag == 0:  # EXACT
                    return t_val
                elif t_flag == 1:  # LOWER BOUND
                    alpha = max(alpha, t_val)
                elif t_flag == 2:  # UPPER BOUND
                    beta = min(beta, t_val)
                if alpha >= beta:
                    return t_val

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

        if depth < 100:
            killers = self.killer_moves[depth]
            valid_killers = [k for k in killers if k in moves]
            vk_set = set(valid_killers)
            other_moves = [m for m in moves if m not in vk_set]
            moves = valid_killers + other_moves

        alpha_original = alpha
        beta_original = beta
        best_val = float("-inf") if maximizing_player else float("inf")

        if maximizing_player:
            for i, move in enumerate(moves):
                # --- Late Move Reduction (LMR) ---
                do_lmr = False
                if depth > 3 and i > 4 and best_val > float("-inf"):
                    is_promising = False
                    for dr, dc in board.get_row_directions(move[0]):
                        nr, nc = move[0] + dr, move[1] + dc
                        if 0 <= nr < board.size and 0 <= nc < board.size:
                            # Check if ANY piece is neighbor (tactical/blocking)
                            if board.board[nr][nc] != 0:
                                is_promising = True
                                break

                    if not is_promising:
                        do_lmr = True

                # Apply move (Backtracking)
                board.board[move[0]][move[1]] = self.player_id

                val = float("-inf")
                if do_lmr:
                    # Reduced search
                    val = self.minimax(board, depth - 2, False, alpha, beta)
                    # Re-search if result improves alpha (found better move than expected)
                    if val > alpha:
                        val = self.minimax(board, depth - 1, False, alpha, beta)
                else:
                    val = self.minimax(board, depth - 1, False, alpha, beta)

                board.board[move[0]][move[1]] = 0  # Undo

                if val > best_val:
                    best_val = val
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    if depth < 100:
                        self.store_killer_move(depth, move)
                    break
        else:
            opponent = 3 - self.player_id
            for i, move in enumerate(moves):
                # --- Late Move Reduction (LMR) ---
                do_lmr = False
                if depth > 3 and i > 4 and best_val < float("inf"):
                    is_promising = False
                    for dr, dc in board.get_row_directions(move[0]):
                        nr, nc = move[0] + dr, move[1] + dc
                        if 0 <= nr < board.size and 0 <= nc < board.size:
                            if board.board[nr][nc] != 0:
                                is_promising = True
                                break

                    if not is_promising:
                        do_lmr = True

                # Apply move (Backtracking)
                board.board[move[0]][move[1]] = opponent

                val = float("inf")
                if do_lmr:
                    val = self.minimax(board, depth - 2, True, alpha, beta)
                    # Re-search if result improves beta (found better move for minimizer)
                    if val < beta:
                        val = self.minimax(board, depth - 1, True, alpha, beta)
                else:
                    val = self.minimax(board, depth - 1, True, alpha, beta)

                board.board[move[0]][move[1]] = 0  # Undo

                if val < best_val:
                    best_val = val
                beta = min(beta, best_val)
                if beta <= alpha:
                    if depth < 100:
                        self.store_killer_move(depth, move)
                    break

        # --- Transposition Table Store ---
        tt_flag = 0  # EXACT
        if best_val <= alpha_original:
            tt_flag = 2  # UPPER
        elif best_val >= beta_original:
            tt_flag = 1  # LOWER

        self.transposition_table[board_hash] = (depth, tt_flag, best_val)

        return best_val

    def store_killer_move(self, depth, move):
        # Shift killers: [1] becomes old [0], [0] becomes new move
        if self.killer_moves[depth][0] != move:
            self.killer_moves[depth][1] = self.killer_moves[depth][0]
            self.killer_moves[depth][0] = move

    def get_board_hash(self, board: HexBoard, maximizing_player: bool):
        """Creates a unique hashable representation of the board state."""
        # Convert mutable list of lists to immutable tuple of tuples, and include player turn
        return (tuple(tuple(row) for row in board.board), maximizing_player)

    def get_relevant_moves(self, board: HexBoard):
        """
        Generates candidate moves from the active zone.
        Uses direct neighbors (Distance 1) by default and expands to Distance 2 only when needed.
        """
        occupied = []
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] != 0:
                    occupied.append((r, c))

        if not occupied:
            return self.get_possible_moves(board)

        relevant_d1 = set()
        neighbors_d1_by_piece = {}

        # Helper to check bounds
        def is_valid(r, c):
            return 0 <= r < board.size and 0 <= c < board.size

        for r, c in occupied:
            # Check all neighbors (Distance 1)
            neighbors_d1 = []
            for dr, dc in board.get_row_directions(r):
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc):
                    if board.board[nr][nc] == 0:
                        relevant_d1.add((nr, nc))
                        neighbors_d1.append((nr, nc))
            neighbors_d1_by_piece[(r, c)] = neighbors_d1

        moves = list(relevant_d1)

        # Controlled fallback: add Distance 2 only if Distance 1 produced too few options.
        min_active_moves = min(8, board.size * 2)
        if len(moves) >= min_active_moves:
            return moves

        relevant = set(relevant_d1)

        for r, c in occupied:
            # Check Bridge Endpoints (Distance 2 via empty neighbor)
            neighbors_d1 = neighbors_d1_by_piece[(r, c)]
            for r1, c1 in neighbors_d1:
                # Expand from the empty neighbor
                for dr, dc in board.get_row_directions(r1):
                    r2, c2 = r1 + dr, c1 + dc
                    if is_valid(r2, c2) and board.board[r2][c2] == 0:
                        relevant.add((r2, c2))

        # Convert to list
        moves = list(relevant)

        return moves

    def order_moves(self, board: HexBoard, moves: list):
        """
        Sorts moves to maximize pruning efficiency.
        Prioritizes forcing moves (blocking), connectivity, and center proximity.
        """
        center = board.size // 2

        def quick_score(move):
            r, c = move
            # Distance to center
            dist_center = abs(r - center) + abs(c - center)

            # Allied and opponent neighbors
            my_neighbors = 0
            op_neighbors = 0
            opponent_id = 3 - self.player_id
            for dr, dc in board.get_row_directions(r):
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.size and 0 <= nc < board.size:
                    if board.board[nr][nc] == self.player_id:
                        my_neighbors += 1
                    elif board.board[nr][nc] == opponent_id:
                        op_neighbors += 1

            # Score: High weight for building our bridges and blocking opponent's.
            # Slight penalty for distance from center.
            return (my_neighbors * 10) + (op_neighbors * 10) - dist_center

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
        Advanced Heuristic: Two-Path Robustness
        Instead of just one path, we evaluate the cost of a secondary disjoint path.
        Formula: (Opponent_Path1 + Opponent_Path2) - (My_Path1 + My_Path2)
        """
        # Calculate Primary Paths
        my_dist_1, my_path_1 = self.calculate_distance(board, self.player_id)
        op_dist_1, op_path_1 = self.calculate_distance(board, 3 - self.player_id)

        # Calculate Secondary Paths (avoiding the primary path nodes)
        # We pass the primary path set to be treated as high-cost obstacles
        my_dist_2, _ = self.calculate_distance(
            board, self.player_id, avoid_nodes=my_path_1
        )
        op_dist_2, _ = self.calculate_distance(
            board, 3 - self.player_id, avoid_nodes=op_path_1
        )

        # Weighting: Primary path is most important, secondary provides security.
        # If secondary path is infinite (blocked), the score should reflect vulnerability.

        my_score = my_dist_1 * 1.5 + my_dist_2 * 0.5
        op_score = op_dist_1 * 1.5 + op_dist_2 * 0.5

        return op_score - my_score

    def calculate_distance(
        self, board: HexBoard, player_id: int, avoid_nodes=None
    ) -> tuple:
        """
        Dijkstra's Algorithm to find shortest path cost.
        Returns (cost, method_used_path_set).
        """
        if avoid_nodes is None:
            avoid_nodes = set()

        size = board.size
        # Priority Queue: (cost, r, c)
        pq = []
        dists = {}  # Sparse dictionary for visited nodes

        # Initial set up based on player direction
        # Player 1: Left-Right (Col 0 to Size-1)
        # Player 2: Top-Bottom (Row 0 to Size-1)

        # Initialize PQ
        if player_id == 1:  # Left -> Right
            for r in range(size):
                cell_cost = self.get_cell_cost(
                    board.board[r][0], player_id, (r, 0) in avoid_nodes
                )
                heapq.heappush(pq, (cell_cost, r, 0))
                dists[(r, 0)] = cell_cost
        else:  # Top -> Bottom
            for c in range(size):
                cell_cost = self.get_cell_cost(
                    board.board[0][c], player_id, (0, c) in avoid_nodes
                )
                heapq.heappush(pq, (cell_cost, 0, c))
                dists[(0, c)] = cell_cost

        parent_map = {}  # To reconstruct path

        while pq:
            current_cost, r, c = heapq.heappop(pq)

            # Pruning
            if current_cost > dists.get((r, c), float("inf")):
                continue

            # Check Reached Target
            if (player_id == 1 and c == size - 1) or (player_id == 2 and r == size - 1):
                path = set()
                curr = (r, c)
                while curr in parent_map:
                    path.add(curr)
                    curr = parent_map[curr]
                path.add(curr)
                return current_cost, path

            # Neighbors
            for dr, dc in board.get_row_directions(r):
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size:
                    new_cost = current_cost + self.get_cell_cost(
                        board.board[nr][nc], player_id, (nr, nc) in avoid_nodes
                    )

                    if new_cost < dists.get((nr, nc), float("inf")):
                        dists[(nr, nc)] = new_cost
                        parent_map[(nr, nc)] = (r, c)
                        heapq.heappush(pq, (new_cost, nr, nc))

        return 9999, set()  # No path found

    def get_cell_cost(self, cell_value, player_id, is_avoided=False):
        """
        Determines the traversal cost of a cell.
        """
        if is_avoided:
            return 50  # High penalty but passable if desperate

        if cell_value == player_id:
            return 0  # Existing connection
        elif cell_value == 0:
            return 1  # Empty cell (needs 1 move)
        else:
            return 100  # Opponent block (effectively infinite)

    def is_board_empty(self, board):
        for row in board.board:
            for cell in row:
                if cell != 0:
                    return False
        return True
