# player.py - Implementación del jugador IA para Hex
"""
Módulo que contiene la clase Player que representa al jugador de IA.
Este es el punto de entrada principal que será llamado por el sistema de juego.
"""


class Player:
    """
    Clase que representa al jugador de IA para el juego Hex.

    Attributes:
        color (int): El color del jugador (1 o 2)
        board_size (int): El tamaño del tablero
    """

    def __init__(self, color: int, board_size: int = 11):
        """
        Inicializa el jugador.

        Args:
            color: El color asignado al jugador (1 o 2)
            board_size: El tamaño del tablero (por defecto 11x11)
        """
        self.color = color
        self.board_size = board_size
        # TODO: Inicializar estructuras de datos necesarias

    def get_move(self, board: list) -> tuple:
        """
        Determina el mejor movimiento a realizar.

        Args:
            board: Matriz 2D que representa el estado actual del tablero.
                   0 = vacío, 1 = jugador 1, 2 = jugador 2

        Returns:
            tuple: (fila, columna) del movimiento elegido
        """
        # TODO: Implementar lógica de selección de movimiento
        # - Usar minimax con poda alfa-beta
        # - Aplicar heurísticas de evaluación
        # - Considerar tiempo límite
        raise NotImplementedError("Implementar get_move")

    def _minimax(
        self, board: list, depth: int, alpha: float, beta: float, maximizing: bool
    ) -> tuple:
        """
        Algoritmo Minimax con poda alfa-beta.

        Args:
            board: Estado actual del tablero
            depth: Profundidad máxima de búsqueda
            alpha: Valor alfa para la poda
            beta: Valor beta para la poda
            maximizing: True si es turno del maximizador

        Returns:
            tuple: (valor, mejor_movimiento)
        """
        # TODO: Implementar minimax con poda alfa-beta
        raise NotImplementedError("Implementar _minimax")

    def _get_valid_moves(self, board: list) -> list:
        """
        Obtiene todos los movimientos válidos (celdas vacías).

        Args:
            board: Estado actual del tablero

        Returns:
            list: Lista de tuplas (fila, columna) de movimientos válidos
        """
        # TODO: Implementar generación de movimientos válidos
        raise NotImplementedError("Implementar _get_valid_moves")

    def _evaluate(self, board: list) -> float:
        """
        Evalúa el estado actual del tablero.

        Args:
            board: Estado actual del tablero

        Returns:
            float: Valor heurístico del estado
        """
        # TODO: Implementar función de evaluación heurística
        raise NotImplementedError("Implementar _evaluate")

    def _check_winner(self, board: list) -> int:
        """
        Verifica si hay un ganador.

        Args:
            board: Estado actual del tablero

        Returns:
            int: 0 si no hay ganador, 1 o 2 si hay ganador
        """
        # TODO: Implementar detección de ganador (camino conectado)
        raise NotImplementedError("Implementar _check_winner")
