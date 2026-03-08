# HEXABEL - Jugador de IA para Hex

## Descripción

Implementación de un jugador de inteligencia artificial para el juego de tablero Hex.

## Estructura del Proyecto

```
HEXABEL/
├── solution.py      # Archivo principal de solución (obligatorio)
├── player.py        # Implementación del jugador IA
├── board.py         # Utilidades del tablero
├── test_game.py     # Tests y simulación
├── requirements.txt # Dependencias
└── README.md        # Este archivo
```

## Reglas del Juego Hex

- Tablero romboidal de 11x11 (por defecto)
- Dos jugadores alternan turnos colocando fichas
- **Jugador 1**: Conectar borde Norte con borde Sur
- **Jugador 2**: Conectar borde Este con borde Oeste
- No hay empates en Hex

## Uso

```python
from solution import HexPlayer

# Crear jugador
player = HexPlayer(color=1)  # 1 o 2

# Obtener movimiento
board = [[0]*11 for _ in range(11)]
move = player.play(board)
print(f"Movimiento: {move}")
```

## Tests

```bash
python test_game.py
```

## TODO

- [ ] Implementar minimax con poda alfa-beta
- [ ] Implementar función de evaluación heurística
- [ ] Implementar detección de ganador
- [ ] Optimizar tiempo de respuesta

## Autor

Abel de la Noval Pérez
