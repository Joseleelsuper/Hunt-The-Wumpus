import pygame
import os
import numpy as np


class PygameMode:
    def __init__(self, board):
        self.board = board
        pygame.init()
        self.calculate_cell_size()
        self.width = self.board.size * self.cell_size
        self.height = self.board.size * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hunt the Wumpus")

        self.load_images()
        self.font = pygame.font.Font(
            None, max(12, self.cell_size // 4)
        )  # Ajustar tamaño de fuente
        self.clock = pygame.time.Clock()
        self.QUIT = pygame.QUIT

    def calculate_cell_size(self):
        max_width = 800  # Tamaño máximo de la ventana
        self.cell_size = min(
            max_width // self.board.size, 100
        )  # Limitar el tamaño máximo de celda a 100 píxeles

    def load_images(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
        self.images = {
            "A": pygame.image.load(os.path.join(base_path, "agent.png")),
            "W": pygame.image.load(os.path.join(base_path, "wumpus.png")),
            "G": pygame.image.load(os.path.join(base_path, "gold.png")),
            "O": pygame.image.load(os.path.join(base_path, "pit.png")),
            "b": pygame.image.load(os.path.join(base_path, "breeze.png")),
            "s": pygame.image.load(os.path.join(base_path, "stench.png")),
        }
        for key in self.images:
            self.images[key] = pygame.transform.scale(
                self.images[key], (self.cell_size, self.cell_size)
            )

    def calculate_utility(self):
        utility = np.zeros((self.board.size, self.board.size))
        gold_pos = self.board.gold_pos
        for i in range(self.board.size):
            for j in range(self.board.size):
                if (i, j) == gold_pos:
                    utility[i][j] = 0  # El oro tiene el menor coste.
                elif "W" in self.board.board[i][j] or "O" in self.board.board[i][j]:
                    utility[i][j] = 1000  # Wumpus y pozos tienen el mayor coste
                else:
                    distance = abs(i - gold_pos[0]) + abs(j - gold_pos[1])
                    utility[i][
                        j
                    ] = distance  # El coste es directamente proporcional a la distancia
        return utility

    def get_events(self):
        return pygame.event.get()

    def run(self):
        running = True
        while running:
            for event in self.get_events():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.board.move_agent("up")
                    elif event.key == pygame.K_s:
                        self.board.move_agent("down")
                    elif event.key == pygame.K_a:
                        self.board.move_agent("left")
                    elif event.key == pygame.K_d:
                        self.board.move_agent("right")
                    elif event.key == pygame.K_SPACE:
                        if not self.board.arrowAvailable:
                            print("No tienes flechas disponibles.")
                        else:
                            direction = input(
                                "Ingresa una dirección para disparar (W/A/S/D): "
                            ).lower()
                            direction_map = {
                                "w": "up",
                                "a": "left",
                                "s": "down",
                                "d": "right",
                            }
                            if direction in direction_map:
                                hit, message = self.board.shoot_arrow(
                                    direction_map[direction]
                                )
                                print(message)
                            else:
                                print("Dirección inválida.")

            self.draw_board()
            pygame.display.flip()

            game_over, message = self.board.check_game_over()
            if game_over:
                print(message)
                pygame.time.wait(2000)
                running = False

            self.clock.tick(30)

        pygame.quit()

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        board = self.board.get_board()
        utility = self.calculate_utility()
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if not cell:  # Si la celda está vacía
                    utility_value = utility[y][x]
                    text = self.font.render(
                        f"{utility_value:.0f}", True, (100, 100, 100)
                    )
                    text_rect = text.get_rect(
                        center=(
                            x * self.cell_size + self.cell_size // 2,
                            y * self.cell_size + self.cell_size // 2,
                        )
                    )
                    self.screen.blit(text, text_rect)
                for char in cell:
                    if char in self.images:
                        self.screen.blit(
                            self.images[char], (x * self.cell_size, y * self.cell_size)
                        )
        pygame.display.flip()

    def quit(self):
        pygame.quit()

    def show_game_over_screen(self, message):
        # Crear una superficie translúcida
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)  # Valor de transparencia (0-255)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        self.display_message(message)
        self.display_message("Presiona 'R' para reiniciar o 'Q' para salir", offset=50)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        return True  # Reiniciar el juego
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        waiting = False
                        return False  # Salir del juego

    def display_message(self, message, offset=0):
        text_surface = self.font.render(message, True, (255, 255, 255))
        rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 + offset))
        self.screen.blit(text_surface, rect)
