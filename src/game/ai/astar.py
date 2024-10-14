import heapq
import pygame
import time
from ui.pygame_mode import PygameMode

class AStarPlayer:
    def __init__(self, board):
        self.board = board
        self.path = None
        self.game = PygameMode(board)

    def calculate_path(self):
        start = self.board.agent_pos
        goal = self.board.gold_pos
        self.path = self.a_star_search(start, goal)

    def get_best_move(self):
        if self.path is None:
            self.calculate_path()
        
        if self.path and len(self.path) > 1:
            next_pos = self.path[1]
            self.path = self.path[1:]  # Remove the current position
            return self.get_move_direction(self.board.agent_pos, next_pos)
        return None

    def a_star_search(self, start, goal):
        open_list = []
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.board.heuristic(start, goal)}

        heapq.heappush(open_list, (f_score[start], start))

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + self.get_cost(neighbor)

                if neighbor not in [i[1] for i in open_list]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.board.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
                elif tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.board.heuristic(neighbor, goal)
                    if neighbor in closed_set:
                        closed_set.remove(neighbor)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None

    def get_neighbors(self, pos):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if 0 <= new_pos[0] < self.board.size and 0 <= new_pos[1] < self.board.size:
                neighbors.append(new_pos)
        return neighbors

    def get_cost(self, pos):
        cell = self.board.board[pos[0]][pos[1]]
        base_cost = 1

        # Aumentar significativamente el coste para celdas peligrosas
        if 'W' in cell or 'P' in cell:
            return float('inf')  # Coste infinito para Wumpus y pozos
        elif 'b' in cell:
            base_cost *= 50  # Coste muy alto para brisas
        elif 's' in cell:
            base_cost *= 100  # Coste extremadamente alto para hedor

        # Reducir el coste para celdas más cercanas al oro
        distance_to_gold = self.board.heuristic(pos, self.board.gold_pos)
        gold_factor = max(1, self.board.size - distance_to_gold)
        
        return base_cost / gold_factor

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    def get_move_direction(self, from_pos, to_pos):
        dx, dy = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]
        if dx == -1:
            return 'up'
        elif dx == 1:
            return 'down'
        elif dy == -1:
            return 'left'
        elif dy == 1:
            return 'right'

    def run(self):
        running = True
        while running:
            self.board.reset()
            self.path = None
            self.calculate_path()

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