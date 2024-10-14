class TextMode:
    def __init__(self, board):
        self.board = board

    def run(self):
        while True:
            self.display_board()
            action = input("Ingresa una acción (M/D/S para mover/disparar/salir): ").lower()
            
            if action in ['s', 'salir']:
                print("Gracias por jugar. ¡Hasta luego!")
                break
            
            if action in ['m', 'mover']:
                direction = input("Ingresa una dirección (W/A/S/D): ").lower()
                direction_map = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}
                if direction in direction_map:
                    self.board.move_agent(direction_map[direction])
                else:
                    print("Dirección inválida.")
            
            elif action in ['d', 'disparar']:
                direction = input("Ingresa una dirección para disparar (W/A/S/D): ").lower()
                direction_map = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}
                if direction in direction_map:
                    if self.board.shoot_arrow(direction_map[direction]):
                        print("¡Has matado al Wumpus!")
                    else:
                        print("Has fallado.")
                else:
                    print("Dirección inválida.")
            
            else:
                print("Acción inválida.")
            
            game_over, message = self.board.check_game_over()
            if game_over:
                self.display_board()
                print(message)
                break

    def display_board(self):
        board = self.board.get_board()
        horizontal_line = '+---' * self.board.size + '+'
        
        print(horizontal_line)
        for row in board:
            row_str = '|'
            for cell in row:
                cell_content = ''.join(sorted(cell))[:3].ljust(3)  # Limita a 4 caracteres y rellena con espacios
                row_str += f'{cell_content}|'
            print(row_str)
            print(horizontal_line)
        print()