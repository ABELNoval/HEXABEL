from board import HexBoard
from solution import SmartPlayer


def print_board(board: HexBoard):
    """Imprime el tablero de manera simple"""
    size = board.size
    print("  " + " ".join(str(i) for i in range(size)))  # Column indices
    for r in range(size):
        # offset para simular tablero hex
        print(" " * r + str(r) + " ", end="")  # Row index
        row_str = []
        for cell in board.board[r]:
            if cell == 0:
                row_str.append(".")
            elif cell == 1:
                row_str.append("X")  # Jugador 1
            elif cell == 2:
                row_str.append("O")  # Jugador 2
        print(" ".join(row_str))
    print("\n")


def simple_game():
    size = 7  # tamaño del tablero para testeo
    board = HexBoard(size)

    # Crear dos jugadores
    player1 = SmartPlayer(1)
    player2 = SmartPlayer(2)

    current_player = player1
    print("Estado inicial del tablero:")
    print_board(board)

    move_count = 0
    max_moves = size * size

    while move_count < max_moves:
        # Llamar al play() del jugador
        move = current_player.play(board)

        if move is None:
            print(f"Jugador {current_player.player_id} no tiene movimientos válidos.")
            break

        # Colocar ficha
        row, col = move
        if board.board[row][col] != 0:
            print(
                f"Error: Jugador {current_player.player_id} intentó mover a una casilla ocupada ({row},{col})"
            )
            break

        board.board[row][col] = current_player.player_id

        # Mostrar tablero
        print("-" * 20)
        print(f"Jugador {current_player.player_id} juega en ({row},{col})")
        print_board(board)

        # Verificar victoria
        if board.check_connection(current_player.player_id):
            print(f"¡El jugador {current_player.player_id} ha ganado!")
            break

        # Alternar jugadores
        current_player = player2 if current_player == player1 else player1
        move_count += 1

    print("Juego terminado (simulación simple).")


if __name__ == "__main__":
    simple_game()
