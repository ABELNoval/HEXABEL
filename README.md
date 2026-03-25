# HEXABEL ♟️

**HEXABEL** es un agente inteligente diseñado para jugar al juego de estrategia **Hex**, implementado mediante técnicas clásicas de Inteligencia Artificial basadas en búsqueda en árboles de decisión y evaluación heurística.

---

## 📌 Descripción del proyecto

El objetivo de este proyecto es desarrollar una IA capaz de tomar decisiones estratégicas en el juego de Hex, evaluando el estado del tablero y anticipando posibles jugadas futuras.

El agente analiza múltiples configuraciones del juego utilizando un algoritmo de búsqueda y selecciona la acción que maximiza sus probabilidades de victoria mediante una función heurística especializada.

---

## 🧠 Enfoque de la solución

La solución se basa en tres componentes principales:

- **Modelado del juego**: Representación del tablero de Hex, sus reglas y condiciones de victoria.
- **Algoritmo de búsqueda**: Implementación del algoritmo **Minimax**, que permite explorar posibles jugadas futuras considerando tanto el comportamiento del agente como el del oponente.
- **Función heurística**: Evaluación de estados intermedios del tablero para estimar qué jugador tiene ventaja sin necesidad de alcanzar un estado terminal.

---

## 🔍 Algoritmo principal: Minimax

El agente utiliza el algoritmo **Minimax**, una técnica clásica en juegos de dos jugadores con suma cero, donde:

- Un jugador intenta **maximizar** la evaluación del estado.
- El oponente intenta **minimizarla**.

Este algoritmo permite simular múltiples turnos hacia adelante, evaluando las posibles consecuencias de cada jugada antes de tomar una decisión.

---

## 🧩 Heurística implementada

La función heurística está basada en el concepto de **caminos mínimos en grafos**, adaptado al tablero de Hex.

Se compone de los siguientes elementos:

- **Camino mínimo principal**: Calcula la distancia más corta necesaria para conectar los lados del tablero.
- **Camino secundario**: Calcula una ruta alternativa, ignorando parcialmente la principal, para medir la robustez de la posición.
- **Penalización por bloqueo**: Las casillas ocupadas por el oponente incrementan el costo del camino.
- **Evaluación diferencial**: Se compara la distancia del jugador con la del oponente para obtener el valor heurístico final.

Esto permite al agente no solo buscar la victoria más rápida, sino construir posiciones estratégicamente sólidas y resistentes.

---

## ⚙️ Optimizaciones implementadas

Para mejorar la eficiencia del algoritmo y reducir el tiempo de decisión, se incorporan técnicas clásicas de optimización en búsqueda:

- **Move Ordering (ordenamiento de movimientos)**: prioriza movimientos prometedores para mejorar la eficiencia de la exploración.
- **Killer Moves**: reutiliza movimientos que previamente generaron podas efectivas en el árbol de búsqueda.
- **Late Move Reduction (LMR)**: reduce la profundidad de exploración en movimientos menos prometedores.
- **Transposition Tables**: almacena evaluaciones de estados previamente visitados para evitar recomputaciones.

Estas optimizaciones permiten reducir significativamente el número de nodos evaluados y mejorar el rendimiento general del agente.

---

## 🗂️ Estructura del proyecto

```id="f0r4px"
HEXABEL/
│
├── board.py        # Representación del tablero y lógica del juego
├── solution.py       # Implementación del agente IA (Minimax + heurística)
├── player.py       # Clase base de Player
├── test_game.py     # Simulación y pruebas de partidas
│
├── README.md
└── .gitignore
```

---

## ▶️ Ejecución

Para ejecutar una simulación del juego:

```bash id="q8m1cz"
python testgame.py
```

Esto ejecutará una partida simulada donde el agente toma decisiones automáticamente.

---

## 🚀 Objetivos del proyecto

- Implementar un agente basado en **Minimax** para el juego de Hex.
- Diseñar una **heurística eficiente basada en grafos**.
- Aplicar técnicas de **optimización en búsqueda**.
- Lograr un equilibrio entre **calidad de decisión y tiempo de ejecución**.

---

## 📚 Aprendizajes

Este proyecto permite comprender de forma práctica:

- Algoritmos de búsqueda adversarial (Minimax).
- Diseño de heurísticas en juegos.
- Técnicas de optimización como LMR, Killer Moves y Transposition Tables.
- Representación de problemas como grafos.

---

## 👤 Autor

**Abel de la Noval Pérez**

---

## 📄 Licencia

Este proyecto se desarrolla con fines académicos.
