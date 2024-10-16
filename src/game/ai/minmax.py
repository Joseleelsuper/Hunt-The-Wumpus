import pygame
import time
from ui.pygame_mode import PygameMode
from copy import deepcopy

class MinMaxPlayer:
    def __init__(self, board, depth_limit=3):
        self.board = board
        self.depth_limit = depth_limit
        self.game = PygameMode(board)

    def get_best_move(self):
        best_move, _ = self.minimax(self.board, 0, True)
        return best_move

    def minimax(self, board, depth, is_maximizing):
        if depth >= self.depth_limit:
            return None, self.evaluate(board)

        game_over, message = board.check_game_over()
        if game_over:
            if message == "¡Has encontrado el oro! ¡Ganaste!":
                return None, float('inf')
            elif message == "¡El Wumpus te ha atrapado!" or message == "¡Has caído en un hoyo!":
                return None, float('-inf')
            else:
                return None, 0

        if is_maximizing:
            best_value = float('-inf')
            best_move = None
            for move in self.get_agent_moves(board):
                new_board = self.simulate_move(board, move)
                _, value = self.minimax(new_board, depth + 1, False)
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_move, best_value
        else:
            best_value = float('inf')
            new_board = self.simulate_dangerous_move(board)
            _, value = self.minimax(new_board, depth + 1, True)
            if value < best_value:
                best_value = value
            return None, best_value

    def evaluate(self, board):
        agent_pos = board.agent_pos
        gold_pos = board.gold_pos
        distance_to_gold = board.heuristic(agent_pos, gold_pos)
        
        danger_penalty = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = agent_pos[0] + dx, agent_pos[1] + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if 'W' in board.board[nx][ny] or 'P' in board.board[nx][ny]:
                    danger_penalty += 10

        return -distance_to_gold - danger_penalty

    def get_agent_moves(self, board):
        return ['up', 'down', 'left', 'right']

    def simulate_move(self, board, move):
        new_board = deepcopy(board)
        new_board.move_agent(move)
        return new_board

    def simulate_dangerous_move(self, board):
        new_board = deepcopy(board)
        new_board.move_dangerous_object()
        return new_board

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
                else:
                    self.board.move_dangerous_object()
                
                time.sleep(0.7)

            if running and not self.board.custom_board:
                print("Generando un nuevo tablero aleatorio...")
            elif running:
                print("Reiniciando el tablero personalizado...")
            
            pygame.time.wait(1000)  # Esperar 1 segundo antes de reiniciar

        self.game.quit()