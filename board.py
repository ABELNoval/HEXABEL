# board.py - Utilidades para el tablero de Hex
"""
Módulo con funciones auxiliares para manipulación y análisis del tablero Hex.
"""

from typing import List, Tuple, Set
from collections import deque


def get_neighbors(row: int, col: int, board_size: int) -> List[Tuple[int, int]]:
    """
    Obtiene los vecinos válidos de una celda en el tablero hexagonal.

    En Hex, cada celda tiene hasta 6 vecinos:
    - (row-1, col), (row-1, col+1)
    - (row, col-1), (row, col+1)
    - (row+1, col-1), (row+1, col)

    Args:
        row: Fila de la celda
        col: Columna de la celda
        board_size: Tamaño del tablero

    Returns:
        Lista de tuplas (fila, columna) de vecinos válidos
    """
    # TODO: Implementar obtención de vecinos hexagonales
    directions = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
    neighbors = []
    # TODO: Filtrar vecinos dentro del tablero
    raise NotImplementedError("Implementar get_neighbors")


def is_valid_position(row: int, col: int, board_size: int) -> bool:
    """
    Verifica si una posición está dentro del tablero.

    Args:
        row: Fila
        col: Columna
        board_size: Tamaño del tablero

    Returns:
        bool: True si la posición es válida
    """
    # TODO: Implementar validación de posición
    raise NotImplementedError("Implementar is_valid_position")


def get_empty_cells(board: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Obtiene todas las celdas vacías del tablero.

    Args:
        board: Matriz del tablero

    Returns:
        Lista de tuplas (fila, columna) de celdas vacías
    """
    # TODO: Implementar búsqueda de celdas vacías
    raise NotImplementedError("Implementar get_empty_cells")


def copy_board(board: List[List[int]]) -> List[List[int]]:
    """
    Crea una copia profunda del tablero.

    Args:
        board: Tablero original

    Returns:
        Copia del tablero
    """
    # TODO: Implementar copia del tablero
    raise NotImplementedError("Implementar copy_board")


def make_move(
    board: List[List[int]], row: int, col: int, player: int
) -> List[List[int]]:
    """
    Realiza un movimiento en el tablero (retorna nueva copia).

    Args:
        board: Tablero actual
        row: Fila del movimiento
        col: Columna del movimiento
        player: Jugador que realiza el movimiento (1 o 2)

    Returns:
        Nuevo tablero con el movimiento aplicado
    """
    # TODO: Implementar aplicación de movimiento
    raise NotImplementedError("Implementar make_move")


def check_connection(board: List[List[int]], player: int) -> bool:
    """
    Verifica si un jugador ha ganado (conexión de lado a lado).

    - Jugador 1: Conecta arriba con abajo (filas)
    - Jugador 2: Conecta izquierda con derecha (columnas)

    Args:
        board: Estado del tablero
        player: Jugador a verificar (1 o 2)

    Returns:
        bool: True si el jugador ha ganado
    """
    # TODO: Implementar BFS/DFS para verificar conexión
    raise NotImplementedError("Implementar check_connection")


def shortest_path_distance(board: List[List[int]], player: int) -> int:
    """
    Calcula la distancia del camino más corto para completar la conexión.
    Útil para la función de evaluación heurística.

    Args:
        board: Estado del tablero
        player: Jugador a evaluar

    Returns:
        int: Distancia mínima (número de celdas vacías necesarias)
             Retorna 0 si ya ganó, infinito si es imposible
    """
    # TODO: Implementar Dijkstra o BFS para camino más corto
    raise NotImplementedError("Implementar shortest_path_distance")


def print_board(board: List[List[int]]) -> None:
    """
    Imprime el tablero de forma visual (hexagonal).

    Args:
        board: Tablero a imprimir
    """
    # TODO: Implementar visualización del tablero
    raise NotImplementedError("Implementar print_board")
