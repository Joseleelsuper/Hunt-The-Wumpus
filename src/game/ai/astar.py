import heapq
import sys
import pygame
import time
import os

from ..board import Board
from ..utils import get_move_direction

# Ajustar el sys.path para permitir imports relativos
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(project_root)

from src.ui.pygame_mode import PygameMode


class AStarPlayer:
    """
    Clase que representa un jugador que utiliza el algoritmo A* para encontrar
    la mejor ruta hacia el oro.
    """

    def __init__(self, board: Board):
        """
        Inicializa el jugador con el tablero en el que se encuentra.

        Args:
            board (Board): Tablero en el que se encuentra el jugador.
        """
        self.board = board
        self.path = None
        self.game = PygameMode(board)

    def calculate_path(self):
        """
        Calcula la ruta óptima hacia el oro utilizando el algoritmo A*.
        """
        start = self.board.agent_pos
        goal = self.board.gold_pos
        self.path = self.a_star_search(start, goal)

    def get_best_move(self):
        """
        Devuelve el siguiente movimiento a realizar en la ruta hacia el oro.

        Returns:
            str: Dirección del movimiento a realizar.
        """
        if self.path is None:
            self.calculate_path()

        if self.path and len(self.path) > 1:
            next_pos = self.path[1]
            self.path = self.path[1:]
            return get_move_direction(self.board.agent_pos, next_pos)
        return None

    def a_star_search(self, start: tuple, goal: tuple):
        """
        Implementación del algoritmo A* para encontrar la ruta óptima entre dos puntos.

        Args:
            start (tuple): Posición de inicio (x, y).
            goal (tuple): Posición de destino (x, y).

        Returns:
            list: Lista de posiciones que forman la ruta óptima.
        """
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
                    f_score[neighbor] = g_score[neighbor] + self.board.heuristic(
                        neighbor, goal
                    )
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
                elif tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.board.heuristic(
                        neighbor, goal
                    )
                    if neighbor in closed_set:
                        closed_set.remove(neighbor)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None

    def get_neighbors(self, pos: tuple):
        """
        Devuelve las posiciones vecinas a una posición dada.

        Args:
            pos (tuple): Posición actual (x, y).

        Returns:
            list: Lista de posiciones vecinas.
        """
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if 0 <= new_pos[0] < self.board.size and 0 <= new_pos[1] < self.board.size:
                neighbors.append(new_pos)
        return neighbors

    def get_cost(self, pos: tuple):
        """
        Calcula el coste de moverse a una posición dada.

        Args:
            pos (tuple): Posición a la que se quiere mover (x, y).

        Returns:
            float: Coste de moverse a la posición dada.
        """
        cell = self.board.board[pos[0]][pos[1]]
        base_cost = 1

        # Aumentar significativamente el coste para celdas peligrosas
        if "W" in cell or "P" in cell:
            return float("inf")
        elif "b" and "s" in cell:
            base_cost *= 150
        elif "b" in cell:
            base_cost *= 50
        elif "s" in cell:
            base_cost *= 100

        # Reducir el coste para celdas más cercanas al oro
        distance_to_gold = self.board.heuristic(pos, self.board.gold_pos)
        gold_factor = max(1, self.board.size - distance_to_gold)

        return base_cost / gold_factor

    def reconstruct_path(self, came_from: dict, current: tuple):
        """
        Reconstruye la ruta óptima a partir de los nodos visitados.

        Args:
            came_from (dict): Diccionario con los nodos visitados.
            current (tuple): Posición actual (x, y).

        Returns:
            list: Lista de posiciones que forman la ruta óptima."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    def run(self):
        """
        Ejecuta el juego y el algoritmo A* para encontrar la ruta óptima hacia el oro.
        """
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
