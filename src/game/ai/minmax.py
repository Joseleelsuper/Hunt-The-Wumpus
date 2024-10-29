import math
import sys
import pygame
import time
import os
from copy import deepcopy

from ..utils import get_agent_moves

# Ajustar el sys.path para permitir imports relativos
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(project_root)

from src.ui.pygame_mode import PygameMode

class MinMaxPlayer:
    def __init__(self, board, depth_limit=6):
        self.board = board
        self.depth_limit = depth_limit
        self.game = PygameMode(board)
        self.recent_moves = []  # Lista para almacenar los movimientos recientes

    def is_move_against_wall(self, board, move):
        previous_pos = board.agent_pos
        new_board = self.simulate_move(board, move)
        new_pos = new_board.agent_pos
        if previous_pos == new_pos:
            return True
        return False

    def get_best_move(self):
        best_move, _ = self.alphabeta(self.board, 0, True, -math.inf, math.inf)
        return best_move

    def alphabeta(self, board, depth, is_maximizing, alpha, beta):
        if depth >= self.depth_limit:
            return None, self.evaluate(board)

        game_over, message = board.check_game_over()
        if game_over:
            if message == "¡Has encontrado el oro! ¡Ganaste!":
                return None, float("inf")
            elif message == "¡El Wumpus te ha atrapado!" or message == "¡Has caído en un hoyo!":
                return None, float("-inf")
            else:
                return None, 0

        if is_maximizing:
            best_value = float("-inf")
            best_move = None
            moves = []
            for move in get_agent_moves():
                if self.is_move_against_wall(board, move):
                    continue
                new_board = self.simulate_move(board, move)
                moves.append((move, new_board))

            for move, new_board in moves:
                _, value = self.alphabeta(new_board, depth + 1, False, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_move, best_value
        else:
            best_value = float("inf")
            for move in get_agent_moves():
                new_board = self.simulate_move(board, move)
                _, value = self.alphabeta(new_board, depth + 1, True, alpha, beta)
                if value < best_value:
                    best_value = value
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return None, best_value

    def is_safe_move(self, board, move):
        """
        Verifica si un movimiento es seguro.
        El agente solo evitará las casillas con peligros reales ('W' o 'P').
        """
        new_board = self.simulate_move(board, move)
        agent_pos = new_board.agent_pos

        # Si la nueva posición es el oro, permitir el movimiento
        if agent_pos == board.gold_pos:
            return True

        # Evitar casillas con peligros reales
        cell = new_board.board[agent_pos[0]][agent_pos[1]]
        if "W" in cell or "P" in cell:
            return False

        return True  # Permitir movimientos a otras casillas, incluso si hay 'S' o 'B'

    def evaluate(self, board):
        """
        Evalúa el tablero y devuelve una puntuación.
        """
        score = 0
        agent_pos = board.agent_pos
        gold_pos = board.gold_pos

        # Distancia de Manhattan al oro
        distance = abs(agent_pos[0] - gold_pos[0]) + abs(agent_pos[1] - gold_pos[1])
        score -= distance

        # Si el agente está en el oro, dar una puntuación alta
        if agent_pos == gold_pos:
            score += 1000

        if "b" or "s" in board.board[agent_pos[0]][agent_pos[1]]:
            score += 100  # Recompensa por detectar peligros

        # Penalización por morir (entrar en un pozo o Wumpus)
        cell = board.board[agent_pos[0]][agent_pos[1]]
        if "W" in cell or "P" in cell:
            score -= 1000  # Penalización alta por morir

        return score

    def simulate_move(self, board, move):
        new_board = deepcopy(board)
        new_board.verbose = False  # Desactivar los prints durante la simulación
        new_board.move_agent(move)
        return new_board

    def check_for_loop(self):
        """
        Verifica si el agente está estancado en un bucle de dos movimientos repetidos tres veces.
        """
        if len(self.recent_moves) < 6:
            return False
        pattern = self.recent_moves[-6:]
        first_move = pattern[0]
        second_move = pattern[1]
        for i in range(0, 6, 2):
            if pattern[i] != first_move or pattern[i+1] != second_move:
                return False
        return True

    def run(self):
        running = True
        while running:
            self.board.reset()
            self.recent_moves = []  # Reiniciar la lista de movimientos
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
                    # Agregar el movimiento a la lista de movimientos recientes
                    self.recent_moves.append(move)
                    if len(self.recent_moves) > 6:
                        self.recent_moves.pop(0)
                else:
                    for move in get_agent_moves():
                        if not self.is_move_against_wall(self.board, move):
                            self.board.move_agent(move)
                            # Agregar el movimiento a la lista de movimientos recientes
                            self.recent_moves.append(move)
                            if len(self.recent_moves) > 6:
                                self.recent_moves.pop(0)
                            break
                self.game.draw_board()
                time.sleep(0.5)

                # Comprobar si el agente está en un bucle
                if self.check_for_loop():
                    print("El agente se ha estancado en un bucle.")
                    # Mostrar mensaje y opciones
                    restart = self.game.show_game_over_screen("El agente se ha estancado en un bucle.")
                    if restart:
                        game_running = False
                    else:
                        game_running = False
                        running = False
                    break

                game_over, message = self.board.check_game_over()
                if game_over:
                    print(message)
                    # Mostrar mensaje y opciones
                    restart = self.game.show_game_over_screen(message)
                    if restart:
                        game_running = False
                    else:
                        game_running = False
                        running = False
                    break
                else:
                    self.board.move_dangerous_object()

                self.game.draw_board()
                time.sleep(0.5)

                game_over, message = self.board.check_game_over()
                if game_over:
                    print(message)
                    # Mostrar mensaje y opciones
                    restart = self.game.show_game_over_screen(message)
                    if restart:
                        game_running = False
                    else:
                        game_running = False
                        running = False
                    break

            if running and not self.board.custom_board:
                print("Generando un nuevo tablero aleatorio...")
            elif running:
                print("Reiniciando el tablero personalizado...")

            pygame.time.wait(1000)

        self.game.quit()