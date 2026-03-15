from player import Player
from board import HexBoard
import random


class SmartPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> tuple:
        """
        Decide la jugada a realizar.
        Por ahora: selecciona una celda vacía aleatoria.
        """

        size = board.size
        grid = board.board

        # Generar lista de movimientos válidos
        moves = []
        for r in range(size):
            for c in range(size):
                if grid[r][c] == 0:
                    moves.append((r, c))

        # Devolver un movimiento válido aleatorio
        if moves:
            return random.choice(moves)

        # Si no hay movimientos, devolver None (no debería pasar)
        return None
