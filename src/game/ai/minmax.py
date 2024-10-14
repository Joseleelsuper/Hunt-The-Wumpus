import math
import pygame
import time
from ui.pygame_mode import PygameMode

class MinMaxPlayer:
    def __init__(self, board, depth_limit=3):
        self.board = board
        self.depth_limit = depth_limit
        self.game = PygameMode(board)
        self.known_board = [[set() for _ in range(board.size)] for _ in range(board.size)]
        self.visited = set()

    def get_best_move(self):
        best_move, _ = self.minimax(self.board.agent_pos, 0, True)
        return best_move

    def minimax(self, node, depth, is_maximizing):
        if depth >= self.depth_limit:
            return None, self.evaluate(node)

        game_over, message = self.board.check_game_over()
        if game_over:
            if message == "¡Has encontrado el oro! ¡Ganaste!":
                return None, float('inf')
            elif message == "¡El Wumpus te ha atrapado!" or message == "¡Has caído en un hoyo!":
                return None, float('-inf')
            else:
                return None, 0

        best_move = None
        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_possible_moves(node):
                self.board.move_agent(move)
                self.update_known_board()
                _, eval = self.minimax(self.board.agent_pos, depth + 1, False)
                self.board.undo_move_agent(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move, max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(node):
                self.board.move_agent(move)
                self.update_known_board()
                _, eval = self.minimax(self.board.agent_pos, depth + 1, True)
                self.board.undo_move_agent(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move, min_eval

    def evaluate(self, node):
        x, y = node
        if 'G' in self.known_board[x][y]:
            return float('inf')
        if 'W' in self.known_board[x][y] or 'P' in self.known_board[x][y]:
            return float('-inf')
        return -self.board.heuristic(node, self.board.gold_pos)

    def get_possible_moves(self, pos):
        moves = []
        for direction in ['up', 'down', 'left', 'right']:
            dx, dy = {
                'up': (-1, 0),
                'down': (1, 0),
                'left': (0, -1),
                'right': (0, 1)
            }[direction]
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < self.board.size and 0 <= new_y < self.board.size:
                moves.append(direction)
        return moves

    def update_known_board(self):
        x, y = self.board.agent_pos
        self.visited.add((x, y))
        self.known_board[x][y] = set(self.board.board[x][y])
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board.size and 0 <= ny < self.board.size:
                self.known_board[nx][ny] = set(self.board.board[nx][ny])

    def run(self):
        running = True
        while running:
            self.board.reset()

            game_running = True
            while game_running:
                for event in self.game.get_events():
                    if event.type == pygame.QUIT:
                        game_running = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_running = False
                            running = False

                move = self.get_best_move()
                if move:
                    self.board.move_agent(move)
                self.game.draw_board()
                
                game_over, message = self.board.check_game_over()
                if game_over:
                    print(message)
                    self.game.draw_board()
                    game_running = False
                
                time.sleep(0.7)

            if running and not self.board.custom_board:
                print("Generando un nuevo tablero aleatorio...")
            elif running:
                print("Reiniciando el tablero personalizado...")
            
            pygame.time.wait(1000)  # Esperar 1 segundo antes de reiniciar

        self.game.quit()