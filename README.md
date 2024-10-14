# Hunt the Wumpus

Este es un juego de Hunt the Wumpus implementado en Python con dos modos de juego: texto y gráfico (usando Pygame), además de una versión de IA que utiliza TensorFlow para aprender a jugar.

## Requisitos

- Python 3.7+
- Pygame
- TensorFlow
- NumPy

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/hunt-the-wumpus.git
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Cómo jugar

Ejecuta el juego con el siguiente comando:

```
python src/main.py
```

Sigue las instrucciones en pantalla para elegir el tamaño del tablero y el modo de juego.

### Modo Texto

- Usa los comandos "mover" y "disparar" seguidos de una dirección (arriba, abajo, izquierda, derecha) para jugar.
- Escribe "salir" para terminar el juego.

### Modo Pygame

- Usa las teclas de flecha para mover al agente.
- Presiona la barra espaciadora para disparar (se te pedirá que ingreses una dirección).

## Reglas del juego

- El objetivo es encontrar el oro sin ser atrapado por el Wumpus o caer en un pozo.
- El agente puede sentir una brisa cerca de un pozo y un hedor cerca del Wumpus.
- El agente tiene una flecha para matar al Wumpus.

¡Buena suerte y diviértete!
```