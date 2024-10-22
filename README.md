

# Hunt the Wumpus - Adaptación

**Autor**: [José Gallardo Caballero](mailto:jgc1031@alu.ubu.es)

**Profesor a cargo de la práctica**: [Pedro Latorre Carmona](mailto:plcarmona@ubu.es)

<table>
    <tr>
        <td align="center"><a href="https://github.com/Joseleelsuper"><img src="https://github.com/Joseleelsuper.png" width="100px;" alt=""/><br /><sub><b>José Gallardo</b></sub></a></td>
        <td align="center"><a href="https://github.com/platorrecarmona"><img src="https://github.com/platorrecarmona.png" width="100px;" alt=""/><br /><sub><b>Pedro Latorre</b></sub></a></td>
    </tr>
</table>

<div align="center">
    <a href="https://www.linkedin.com/in/jose-gallardo-caballero/"><img src="https://img.shields.io/static/v1?message=LinkedIn&logo=linkedin&label=&color=0077B5&logoColor=white&labelColor=&style=for-the-badge" height="35" alt="linkedin logo"></a>
</div>

<br clear="both">
<img src="https://raw.githubusercontent.com/Joseleelsuper/Joseleelsuper/output/snake.svg" alt="Snake animation" />

## Proyecto y Propósito

Este proyecto es una adaptación del clásico juego "Hunt the Wumpus". El objetivo era crear un algoritmo MinMax que jugase por el usuario, pero también tiene una versión de modo texto y gráfico que el usuario puede jugar, y además el modo A\* para encontrar la mejor ruta al Wumpus con un algoritmo distinto.

## Instalación de Requisitos

Para instalar los requisitos necesarios para ejecutar el juego, ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

## Ejecución del Juego
Para ejecutar el juego, utilice el siguiente comando:

```bash
cd src
python main.py
```

Si quiere hacerlo más profesional, puede elegir entre diferentes modos de juego:

- `text`: Modo de texto
- `pygame`: Modo gráfico con Pygame
- `astar`: Modo con inteligencia artificial utilizando el algoritmo A\*
- `minmax`: Modo con inteligencia artificial utilizando el algoritmo MinMax

Ejemplo de ejecución en modo A\* con un tablero personalizado:

```bash
cd src
python main.py -newtablero 1 -tablero tableros/tablero_6x6.txt -gamemode astar
```

Ejemplo de ejecución en modo usuario con un tablero aleatorio de tamaño 6x6:

```bash
cd src
python main.py -newtablero 0 -board 6 -gamemode pygame
```

## Estructura del Código
El proyecto está organizado de la siguiente manera:

- `src/`: Contiene el código fuente del juego.
  - `game/`: Contiene la lógica del juego.
    - `board.py`: Implementa el tablero del juego.
    - `utils.py`: Contiene funciones utilitarias.
    - `ai/`: Contiene los algoritmos de inteligencia artificial.
      - `astar.py`: Implementa el algoritmo A\*.
      - `minmax.py`: Implementa el algoritmo MinMax.
  - `ui/`: Contiene las interfaces de usuario.
    - `text_mode.py`: Implementa la interfaz de usuario en modo texto.
    - `pygame_mode.py`: Implementa la interfaz de usuario en modo gráfico con Pygame.
  - `main.py`: Archivo principal para ejecutar el juego.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el juego.
- `tableros/`: Contiene tableros personalizados para el juego.

## Explicación del Código Paso a Paso

Para ver la explicación del código, abrir el README compatible con [Jupyter Notebook](/README.ipynb)