import os
import argparse
from game.board import Board
from ui.text_mode import TextMode
from ui.pygame_mode import PygameMode
from game.ai.astar import AStarPlayer
from game.ai.minmax import MinMaxPlayer

def load_custom_board(file_path: str):
    """
    Carga un tablero personalizado desde un archivo de texto.
    Se espera que el archivo tenga el siguiente formato:
    - Cada línea representa una fila del tablero.
    - Cada celda de la fila puede contener uno o más elementos separados por comas.
    - Los elementos válidos son:
        - A: agente
        - W: Wumpus
        - O: pozo
        - G: oro
        - b: brisa
        - s: hedor
    - Los elementos se pueden agrupar entre corchetes.

    Args:
        file_path (str): Ruta del archivo de texto.

    Returns:
        list, int: Tablero personalizado y tamaño del tablero.

    Raises:
        ValueError: Si el tablero no es cuadrado o el tamaño no está entre 3 y 20.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    board = []
    for line in lines:
        row = []
        i = 0
        while i < len(line.strip()):
            if line[i] == '[':
                end_bracket = line.index(']', i)
                cell_content = line[i+1:end_bracket]
                row.append(cell_content)
                i = end_bracket + 1
            else:
                row.append(line[i])
                i += 1
        board.append(row)
    
    size = len(board)
    
    if not all(len(row) == size for row in board):
        raise ValueError("El tablero no es cuadrado")
    
    if size < 3 or size > 20:
        raise ValueError("El tamaño del tablero debe estar entre 3x3 y 20x20")
    
    return board, size

def print_help():
    """
    Muestra un mensaje de ayuda con las opciones disponibles.
    """
    help_text = f"""
Uso: python main.py [opciones]

Opciones:
  -h, --help            Muestra este mensaje de ayuda
  -newtablero <0/1>     0 para tablero aleatorio, 1 para tablero personalizado
  -board <size>         Tamaño del tablero (3-20) para tablero aleatorio
  -tablero <filename>   Nombre del archivo del tablero personalizado
  -gamemode <mode>      Modo de juego (texto, pygame, astar, minmax)

Ejemplos:
  python main.py -newtablero 1 -tablero tablero_6x6.txt -gamemode astar
  python main.py -newtablero 0 -board 6 -gamemode pygame
    """
    print(help_text)

def main():
    """
    Función principal del programa.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-newtablero', type=int, choices=[0, 1])
    parser.add_argument('-board', type=int)
    parser.add_argument('-tablero', type=str)
    parser.add_argument('-gamemode', type=str)
    parser.add_argument('-h', '--help', action='store_true')

    args = parser.parse_args()

    if args.help:
        print_help()
        return

    print(f"Bienvenido a Hunt the Wumpus!")

    custom_board = None
    size = None
    game_mode = None

    if args.newtablero is None:
        while True:
            board_choice = input("¿Desea usar un tablero personalizado? (s/n): ").lower()
            if board_choice in ['s', 'n']:
                args.newtablero = 1 if board_choice == 's' else 0
                break
            print(f"Opción no válida. Por favor, ingrese 's' o 'n'.")

    if args.newtablero == 1:
        if args.tablero is None:
            custom_boards_dir = os.path.join(os.path.dirname(__file__), '..', 'tableros')
            print(f"Tableros disponibles:")
            for file in os.listdir(custom_boards_dir):
                if file.endswith('.txt'):
                    print(file)
            args.tablero = input("Ingrese el nombre del archivo del tablero: ")
        
        file_path = os.path.join(os.path.dirname(__file__), '..', 'tableros', args.tablero)
        try:
            custom_board, size = load_custom_board(file_path)
        except Exception as e:
            print(f"Error al cargar el tablero: {e}")
            return
    else:
        if args.board is None:
            while True:
                try:
                    size = int(input("Ingrese el tamaño del tablero (3-20): "))
                    if 3 <= size <= 20:
                        break
                    else:
                        print(f"El tamaño debe estar entre 3 y 20.")
                except ValueError:
                    print(f"Por favor, ingrese un número válido.")
        else:
            size = args.board
            if size < 3 or size > 20:
                print(f"El tamaño del tablero debe estar entre 3 y 20.")
                return

    game_modes = {
        "texto": TextMode,
        "pygame": PygameMode,
        "astar": AStarPlayer,
        "minmax": MinMaxPlayer
    }

    if args.gamemode is None:
        while True:
            game_mode = input(f"Elige el modo de juego ({', '.join(game_modes.keys())}): ").lower()
            if game_mode in game_modes:
                break
            print(f"Modo inválido. Por favor, elige texto, pygame, astar o minmax.")
    else:
        game_mode = args.gamemode.lower()
        if game_mode not in game_modes:
            print(f"Modo de juego inválido. Use -h para ver las opciones disponibles.")
            return

    board = Board(size, custom_board=custom_board)
    game = game_modes[game_mode](board)
    game.run()

if __name__ == "__main__":
    main()