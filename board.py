class HexBoard:
    HEX_DIRECTIONS = [
        (-1, 0),  # arriba
        (-1, 1),  # arriba-derecha
        (0, -1),  # izquierda
        (0, 1),  # derecha
        (1, -1),  # abajo-izquierda
        (1, 0),  # abajo
    ]

    def __init__(self, size: int):
        self.size = size
        self.board = [
            [0 for _ in range(size)] for _ in range(size)
        ]  # 0 = vacío, 1 = jugador1, 2 = jugador2

    def clone(self):
        new_board = HexBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row][col] != 0:
            return False
        self.board[row][col] = player_id
        return True

    def check_connection(self, player_id: int) -> bool:
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]

        def dfs(r, c):
            if visited[r][c] or self.board[r][c] != player_id:
                return False
            visited[r][c] = True

            # Lados de victoria
            if player_id == 1 and c == self.size - 1:  # jugador 1: izquierda -> derecha
                return True
            if player_id == 2 and r == self.size - 1:  # jugador 2: arriba -> abajo
                return True

            for dr, dc in self.HEX_DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if dfs(nr, nc):
                        return True
            return False

        if player_id == 1:  # jugador 1: izquierda -> derecha
            for r in range(self.size):
                if self.board[r][0] == player_id and dfs(r, 0):
                    return True
        else:  # jugador 2: arriba -> abajo
            for c in range(self.size):
                if self.board[0][c] == player_id and dfs(0, c):
                    return True
        return False
