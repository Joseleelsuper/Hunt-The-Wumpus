import math
import random
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
    def __init__(self, board, depth_limit=5):
        self.board = board
        self.depth_limit = depth_limit
        self.game = PygameMode(board)

    def is_move_against_wall(self, board, move):
        previous_pos = self.board.agent_pos
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
            safe_moves = []
            for move in get_agent_moves():
                if self.is_move_against_wall(board, move):
                    continue
                new_board = self.simulate_move(board, move)
                if self.is_safe_move(new_board):
                    safe_moves.append((move, new_board))

            if safe_moves:
                moves = safe_moves
            else:
                moves = [(move, self.simulate_move(board, move)) for move in get_agent_moves()]

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

    def is_safe_move(self, board):
        """
        Verifica si un movimiento es seguro (sin Wumpus ni hoyos).
        """
        agent_pos = board.agent_pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = agent_pos[0] + dx, agent_pos[1] + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if "W" in board.board[nx][ny] or "P" in board.board[nx][ny]:
                    return False
        return True

    def evaluate(self, board):
        """
        Evalúa el tablero y devuelve una puntuación.
        """
        score = 0
        agent_pos = board.agent_pos
        gold_pos = board.gold_pos

        # Distancia de Manhattan al oro
        score -= abs(agent_pos[0] - gold_pos[0]) + abs(agent_pos[1] - gold_pos[1])

        # Penalización por peligros
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = agent_pos[0] + dx, agent_pos[1] + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                if "W" in board.board[nx][ny]:
                    score -= 100  # Penalización alta por Wumpus
                if "P" in board.board[nx][ny]:
                    score -= 100  # Penalización alta por hoyo
                if "B" in board.board[nx][ny]:
                    score -= 10   # Penalización baja por brisa
                if "S" in board.board[nx][ny]:
                    score -= 10   # Penalización baja por hedor
                if "G" in board.board[nx][ny]:
                    score += 1000  # Recompensa por oro

        return score

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
                else:
                    for move in get_agent_moves():
                        if not self.is_move_against_wall(self.board, move):
                            self.board.move_agent(move)
                            break
                self.game.draw_board()
                time.sleep(0.5)

                game_over, message = self.board.check_game_over()
                if game_over:
                    print(message)
                    game_running = False
                else:
                    self.board.move_dangerous_object()

                self.game.draw_board()
                time.sleep(0.5)

                game_over, message = self.board.check_game_over()
                if game_over:
                    print(message)
                    game_running = False

            if running and not self.board.custom_board:
                print("Generando un nuevo tablero aleatorio...")
            elif running:
                print("Reiniciando el tablero personalizado...")

            pygame.time.wait(1000)

        self.game.quit()
