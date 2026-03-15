class Player:
    """
    Clase base proporcionada por los profesores.
    """

    def __init__(self, player_id: int):
        self.player_id = player_id  # 1 = jugador1, 2 = jugador2

    def play(self, board):
        """
        Este método debe ser implementado por el jugador autónomo.
        """
        raise NotImplementedError("¡Implementa este método!")
