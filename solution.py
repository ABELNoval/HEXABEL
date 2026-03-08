# solution.py - Archivo de solución final obligatorio
"""
Archivo principal que exporta la clase HexPlayer.
Este es el archivo que será evaluado por el sistema de competencia.

Uso:
    from solution import HexPlayer
    player = HexPlayer(color=1)
    move = player.play(board)
"""

from player import Player
from board import check_connection, get_neighbors, shortest_path_distance


class HexPlayer:
    """
    Clase principal del jugador de Hex para la competencia.

    Interfaz requerida por el sistema de evaluación.
    """

    def __init__(self, color: int):
        """
        Inicializa el jugador.

        Args:
            color: Color asignado al jugador (1 o 2)
                   - 1: Conecta Norte-Sur (filas)
                   - 2: Conecta Este-Oeste (columnas)
        """
        self.color = color
        self.player = Player(color)

    def play(self, board: list) -> tuple:
        """
        Método principal llamado por el sistema para obtener el movimiento.

        Args:
            board: Matriz NxN representando el estado del tablero.
                   - 0: Celda vacía
                   - 1: Ficha del jugador 1
                   - 2: Ficha del jugador 2

        Returns:
            tuple: (fila, columna) del movimiento elegido.
                   Debe ser una celda vacía válida.

        Raises:
            Exception: Si no puede determinar un movimiento válido.
        """
        # TODO: Implementar lógica de juego
        # Delegar al módulo player
        return self.player.get_move(board)


# Alias para compatibilidad
Player = HexPlayer
