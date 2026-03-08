# test_game.py - Tests y simulación del juego Hex
"""
Módulo de pruebas para verificar la implementación del jugador de Hex.
Incluye tests unitarios y simulación de partidas.
"""

import unittest
from typing import List, Tuple

# Importar módulos del proyecto
from solution import HexPlayer
from board import (
    get_neighbors,
    is_valid_position,
    check_connection,
    get_empty_cells,
    copy_board,
    make_move,
    print_board,
)


def create_empty_board(size: int = 11) -> List[List[int]]:
    """Crea un tablero vacío de tamaño size x size."""
    return [[0 for _ in range(size)] for _ in range(size)]


class TestBoard(unittest.TestCase):
    """Tests para las funciones del tablero."""

    def setUp(self):
        """Configura el entorno de pruebas."""
        self.board_size = 11
        self.board = create_empty_board(self.board_size)

    def test_is_valid_position(self):
        """Prueba la validación de posiciones."""
        # TODO: Implementar tests
        # self.assertTrue(is_valid_position(0, 0, self.board_size))
        # self.assertTrue(is_valid_position(10, 10, self.board_size))
        # self.assertFalse(is_valid_position(-1, 0, self.board_size))
        # self.assertFalse(is_valid_position(11, 0, self.board_size))
        pass

    def test_get_neighbors(self):
        """Prueba la obtención de vecinos hexagonales."""
        # TODO: Implementar tests
        # Centro del tablero debería tener 6 vecinos
        # Esquinas deberían tener 3 vecinos
        # Bordes deberían tener 4 vecinos
        pass

    def test_get_empty_cells(self):
        """Prueba la obtención de celdas vacías."""
        # TODO: Implementar tests
        # Tablero vacío debería tener size*size celdas vacías
        pass

    def test_copy_board(self):
        """Prueba la copia profunda del tablero."""
        # TODO: Implementar tests
        # La copia no debería afectar al original
        pass

    def test_check_connection_player1(self):
        """Prueba detección de victoria para jugador 1 (Norte-Sur)."""
        # TODO: Implementar tests
        # Crear un camino conectado de arriba a abajo
        pass

    def test_check_connection_player2(self):
        """Prueba detección de victoria para jugador 2 (Este-Oeste)."""
        # TODO: Implementar tests
        # Crear un camino conectado de izquierda a derecha
        pass


class TestPlayer(unittest.TestCase):
    """Tests para el jugador de IA."""

    def setUp(self):
        """Configura el entorno de pruebas."""
        self.board_size = 11
        self.board = create_empty_board(self.board_size)

    def test_player_initialization(self):
        """Prueba la inicialización del jugador."""
        player1 = HexPlayer(1)
        player2 = HexPlayer(2)
        self.assertEqual(player1.color, 1)
        self.assertEqual(player2.color, 2)

    def test_valid_move(self):
        """Prueba que el jugador retorna un movimiento válido."""
        # TODO: Implementar tests
        # player = HexPlayer(1)
        # move = player.play(self.board)
        # self.assertIsInstance(move, tuple)
        # self.assertEqual(len(move), 2)
        # row, col = move
        # self.assertTrue(0 <= row < self.board_size)
        # self.assertTrue(0 <= col < self.board_size)
        # self.assertEqual(self.board[row][col], 0)
        pass

    def test_move_on_occupied(self):
        """Prueba que el jugador no elige celdas ocupadas."""
        # TODO: Implementar tests
        pass


class GameSimulator:
    """Simulador de partidas de Hex."""

    def __init__(self, board_size: int = 11):
        """
        Inicializa el simulador.

        Args:
            board_size: Tamaño del tablero
        """
        self.board_size = board_size
        self.board = create_empty_board(board_size)
        self.current_player = 1
        self.move_count = 0

    def play_game(
        self, player1: HexPlayer, player2: HexPlayer, verbose: bool = True
    ) -> int:
        """
        Simula una partida completa entre dos jugadores.

        Args:
            player1: Jugador 1 (Norte-Sur)
            player2: Jugador 2 (Este-Oeste)
            verbose: Si True, imprime el progreso

        Returns:
            int: Color del ganador (1 o 2)
        """
        # TODO: Implementar simulación de partida
        # while not self._game_over():
        #     current = player1 if self.current_player == 1 else player2
        #     move = current.play(self.board)
        #     self._apply_move(move)
        #     if verbose:
        #         print(f"Jugador {self.current_player} juega: {move}")
        #     self.current_player = 3 - self.current_player
        # return self._get_winner()
        raise NotImplementedError("Implementar play_game")

    def _game_over(self) -> bool:
        """Verifica si el juego ha terminado."""
        # TODO: Implementar
        raise NotImplementedError("Implementar _game_over")

    def _apply_move(self, move: Tuple[int, int]) -> None:
        """Aplica un movimiento al tablero."""
        # TODO: Implementar
        raise NotImplementedError("Implementar _apply_move")

    def _get_winner(self) -> int:
        """Retorna el ganador actual o 0 si no hay."""
        # TODO: Implementar
        raise NotImplementedError("Implementar _get_winner")


def run_test_game():
    """Ejecuta una partida de prueba."""
    print("=== Simulación de partida de Hex ===\n")

    # TODO: Descomentar cuando esté implementado
    # player1 = HexPlayer(1)
    # player2 = HexPlayer(2)
    # simulator = GameSimulator(board_size=11)
    # winner = simulator.play_game(player1, player2)
    # print(f"\n¡Ganador: Jugador {winner}!")

    print("Implementación pendiente...")


if __name__ == "__main__":
    # Ejecutar tests unitarios
    print("Ejecutando tests unitarios...\n")
    unittest.main(verbosity=2, exit=False)

    print("\n" + "=" * 50 + "\n")

    # Ejecutar simulación de partida
    run_test_game()
