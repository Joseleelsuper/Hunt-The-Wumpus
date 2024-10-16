import os
from game.board import Board
from ui.text_mode import TextMode
from ui.pygame_mode import PygameMode
from game.ai.astar import AStarPlayer
from game.ai.minmax import MinMaxPlayer

def load_custom_board(file_path):
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

def main():
    print("Bienvenido a Hunt the Wumpus!")
    
    custom_board = None
    size = None
    
    while True:
        board_choice = input("¿Desea usar un tablero personalizado? (s/n): ").lower()
        if board_choice == 's':
            custom_boards_dir = os.path.join(os.path.dirname(__file__), '..', 'tableros')
            print("Tableros disponibles:")
            for file in os.listdir(custom_boards_dir):
                if file.endswith('.txt'):
                    print(file)
            board_file = input("Ingrese el nombre del archivo del tablero: ")
            file_path = os.path.join(custom_boards_dir, board_file)
            try:
                custom_board, size = load_custom_board(file_path)
                break
            except Exception as e:
                print(f"Error al cargar el tablero: {e}")
        elif board_choice == 'n':
            while True:
                try:
                    size = int(input("Ingrese el tamaño del tablero (3-20): "))
                    if 3 <= size <= 20:
                        break
                    else:
                        print("El tamaño debe estar entre 3 y 20.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
            break
        else:
            print("Opción no válida. Por favor, ingrese 's' o 'n'.")

    while True:
        game_modes = {
            "texto": TextMode,
            "pygame": PygameMode,
            "astar": AStarPlayer,
            "minmax": MinMaxPlayer
        }
        mode = input(f"Elige el modo de juego: ({', '.join(game_modes.keys())}): ").lower()

        board = Board(size, custom_board=custom_board)
        if mode in game_modes:
            game = game_modes[mode](board)
            break
        print("Modo inválido. Por favor, elige texto, pygame, astar o minmax.")

    game.run()

if __name__ == "__main__":
    main()