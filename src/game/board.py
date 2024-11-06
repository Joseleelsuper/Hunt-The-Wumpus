import random

from .utils import manhattan_distance


class Board:
    """
    Clase que representa el tablero del juego.
    """

    def __init__(self, size: int = 6, custom_board: list = None, verbose: bool = True):
        """
        Inicializa el tablero con un tamaño y un tablero personalizado opcional.

        Args:
            size (int): Tamaño del tablero.
            custom_board (list): Tablero personalizado.
            verbose (bool): Controla la impresión de percepciones.
        """
        self.size = size
        self.custom_board = custom_board
        self.arrowAvailable = True
        self.verbose = verbose
        self.reset()

    def reset(self):
        """
        Reinicia el tablero una vez que se ha terminado una partida.
        """
        self.board = [[[] for _ in range(self.size)] for _ in range(self.size)]
        self.agent_pos = None
        self.wumpus_pos = None
        self.gold_pos = None
        self.pits = []
        self.arrowAvailable = True

        if self.custom_board:
            self.load_custom_board(self.custom_board)
        else:
            self.initialize_board()

        # Seleccionar aleatoriamente uno de los pozos
        if self.pits:
            self.moving_pit = random.choice(self.pits)

    def load_custom_board(self, custom_board: list):
        """
        Carga un tablero personalizado en el tablero.

        Args:
            custom_board (list): Tablero personalizado.

        Raises:
            ValueError: Si el tablero personalizado no contiene un agente o oro.
        """
        for i in range(self.size):
            for j in range(self.size):
                cell_content = custom_board[i][j]
                if (
                    isinstance(cell_content, str)
                    and cell_content.startswith("[")
                    and cell_content.endswith("]")
                ):
                    cell_content = cell_content[1:-1]

                for char in cell_content:
                    if char == "A":
                        self.agent_pos = (i, j)
                        self.board[i][j].append("A")
                    elif char == "W":
                        self.wumpus_pos = (i, j)
                        self.board[i][j].append("W")
                    elif char == "O":
                        self.pits.append((i, j))
                        self.board[i][j].append("O")
                    elif char == "G":
                        self.gold_pos = (i, j)
                        self.board[i][j].append("G")
                    elif char == "b":
                        self.board[i][j].append("b")
                    elif char == "s":
                        self.board[i][j].append("s")

        if not self.agent_pos:
            raise ValueError("El tablero personalizado debe contener un agente (A)")
        if not self.gold_pos:
            raise ValueError("El tablero personalizado debe contener oro (G)")

    def initialize_board(self):
        """
        Inicializa el tablero con los elementos del juego.

        - El agente se coloca en la esquina inferior izquierda.
        - El Wumpus, el oro y los pozos se colocan aleatoriamente.
        - Se colocan las percepciones de brisa y hedor en las celdas adyacentes a los pozos y al Wumpus.
        """
        self.place_agent()
        self.place_wumpus()
        self.place_gold()
        self.place_pits()
        self.place_breezes_and_stenches()

    def place_agent(self):
        """
        Coloca el agente en la esquina inferior izquierda del tablero.
        """
        self.agent_pos = (self.size - 1, 0)
        self.board[self.agent_pos[0]][self.agent_pos[1]].append("A")

    def place_wumpus(self):
        """
        Coloca el Wumpus en una celda aleatoria del tablero.
        """
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.is_valid_placement(x, y):
                self.wumpus_pos = (x, y)
                self.board[x][y].append("W")
                break

    def place_gold(self):
        """
        Coloca el oro en una celda aleatoria del tablero.
        """
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.is_valid_placement(x, y):
                self.gold_pos = (x, y)
                self.board[x][y].append("G")
                break

    def place_pits(self):
        """
        Coloca los pozos en celdas aleatorias del tablero.

        El número de pozos se calcula como el 10% del tamaño del tablero.
        Es decir, si el tablero es de 6x6, se colocarán 3 pozos.
        """
        num_pits = self.size * self.size // 10
        for _ in range(num_pits):
            while True:
                x, y = random.randint(0, self.size - 1), random.randint(
                    0, self.size - 1
                )
                if self.is_valid_placement(x, y) and not self.is_wumpus_or_pit(x, y):
                    self.pits.append((x, y))
                    self.board[x][y].append("O")
                    break

    def is_valid_placement(self, x: int, y: int):
        """
        Comprueba si una celda es una posición válida para colocar un objeto.

        Args:
            x (int): Coordenada x de la celda.
            y (int): Coordenada y de la celda.
        """
        if (
            (x, y) == self.agent_pos
            or (x, y) in self.pits
            or (x, y) == self.wumpus_pos
            or (x, y) == self.gold_pos
        ):
            return False
        return manhattan_distance(x, y, self.agent_pos[0], self.agent_pos[1]) > 2

    def is_wumpus_or_pit(self, x: int, y: int):
        """
        Comprueba si una celda contiene el Wumpus o un pozo.

        Args:
            x (int): Coordenada x de la celda.
            y (int): Coordenada y de la celda.

        Returns:
            bool: True si la celda contiene el Wumpus o un pozo, False en caso contrario.
        """
        return "W" in self.board[x][y] or "O" in self.board[x][y]

    def place_breezes_and_stenches(self):
        """
        Coloca las percepciones de brisa y hedor en las celdas adyacentes a los pozos y al Wumpus.
        """
        for x in range(self.size):
            for y in range(self.size):
                if "O" in self.board[x][y]:
                    self.place_perception(x, y, "b")
                elif "W" in self.board[x][y]:
                    self.place_perception(x, y, "s")

    def place_perception(self, x: int, y: int, perception: str):
        """
        Coloca una percepción en las celdas adyacentes a una celda.

        Args:
            x (int): Coordenada x de la celda.
            y (int): Coordenada y de la celda.
            perception (str): Percepción a colocar (brisa o hedor).
        """
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if (
                    perception not in self.board[nx][ny]
                    and "O" not in self.board[nx][ny]
                    and "W" not in self.board[nx][ny]
                ):
                    self.board[nx][ny].append(perception)

    def get_board(self):
        """
        Devuelve el tablero actual.
        """
        return self.board

    def move_agent(self, direction: str):
        """
        Mueve el agente en una dirección dada.

        Args:
            direction (str): Dirección en la que mover el agente.

        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        dx, dy = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}.get(direction)

        new_x, new_y = self.agent_pos[0] + dx, self.agent_pos[1] + dy

        if 0 <= new_x < self.size and 0 <= new_y < self.size:
            if "A" in self.board[self.agent_pos[0]][self.agent_pos[1]]:
                self.board[self.agent_pos[0]][self.agent_pos[1]].remove("A")
            self.agent_pos = (new_x, new_y)
            if "A" not in self.board[new_x][new_y]:
                self.board[new_x][new_y].append("A")
            self.check_perceptions()
            return True
        return False

    def check_perceptions(self):
        """
        Comprueba las percepciones en la celda actual del agente.
        """
        x, y = self.agent_pos
        perceptions = []
        if "b" in self.board[x][y]:
            perceptions.append("Sientes una brisa. Debe haber un hoyo cerca.")
        if "s" in self.board[x][y]:
            perceptions.append("Percibes un hedor. El Wumpus debe estar cerca.")

        if perceptions and self.verbose:
            print("\n".join(perceptions))

    def shoot_arrow(self, direction: str):
        """
        Dispara una flecha en una dirección dada.

        Args:
            direction (str): Dirección en la que disparar la flecha.

        Returns:
            bool: True si se ha matado al Wumpus, False en caso contrario.
        """
        if not self.arrowAvailable:
            return False, "No tienes flechas disponibles."

        dx, dy = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}[
            direction
        ]

        # Si la dirección no es válida, no se dispara la flecha
        if not (0 <= self.agent_pos[0] + dx < self.size and 0 <= self.agent_pos[1] + dy < self.size):
            return False, "Dirección inválida."

        self.arrowAvailable = False
        
        x, y = self.agent_pos[0] + dx, self.agent_pos[1] + dy
        if "W" in self.board[x][y]:
            self.board[x][y].remove("W")
            self.board[x][y].append("X")  # X represents dead Wumpus
            self.wumpus_pos = None
            self.remove_stench()
            return True, "¡Has matado al Wumpus!"
        return False, "Has fallado."

    def remove_stench(self):
        for x in range(self.size):
            for y in range(self.size):
                if "s" in self.board[x][y]:
                    self.board[x][y].remove("s")

    def check_game_over(self):
        """
        Comprueba si el juego ha terminado.

        Returns:
            bool, str: True si el juego ha terminado, mensaje de finalización en caso contrario.
        """
        x, y = self.agent_pos
        if "W" in self.board[x][y]:
            return True, "¡El Wumpus te ha atrapado!"
        if "O" in self.board[x][y]:
            return True, "¡Has caído en un hoyo!"
        if "G" in self.board[x][y]:
            return True, "¡Has encontrado el oro! ¡Ganaste!"
        return False, None

    def heuristic(self, a: tuple, b: tuple):
        """
        Calcula la heurística entre dos posiciones.

        Args:
            a (tuple): Posición (x, y) de la primera celda.
            b (tuple): Posición (x, y) de la segunda celda.

        Returns:
            int: Heurística entre las dos posiciones.
        """
        return manhattan_distance(a[0], a[1], b[0], b[1])

    def move_dangerous_object(self):
        """
        Mueve el Wumpus o el pozo seleccionado a una nueva posición en el tablero.
        Returns:
            bool: True si se ha movido un objeto, False en caso contrario.
        """

        obj_type, obj_pos = ("O", self.moving_pit)

        possible_moves = self.get_possible_moves(obj_pos)
        agent_pos = self.agent_pos

        if agent_pos in possible_moves:
            new_pos = agent_pos
        else:
            new_pos = self.get_best_move_for_object(possible_moves)

        self.move_object(obj_type, obj_pos, new_pos)

        if obj_type == "O":
            self.moving_pit = new_pos  # Actualizar la posición del pozo

        return True

    def get_best_move_for_object(self, possible_moves: list):
        """
        Devuelve el mejor movimiento para un objeto en una posición dada.

        Args:
            possible_moves (list): Lista de movimientos posibles.

        Returns:
            tuple: Mejor movimiento para el objeto.
        """
        best_move = None
        best_value = float("inf")
        for move in possible_moves:
            value = self.heuristic(move, self.agent_pos)
            if value < best_value:
                best_value = value
                best_move = move
        return best_move

    def move_object(self, obj_type: str, old_pos: tuple, new_pos: tuple):
        """
        Mueve un objeto a una nueva posición en el tablero.

        Args:
            obj_type (str): Tipo de objeto a mover (Wumpus o pozo).
            old_pos (tuple): Posición actual del objeto.
            new_pos (tuple): Nueva posición del objeto.
        """
        x, y = old_pos
        new_x, new_y = new_pos

        if obj_type in self.board[x][y]:
            self.board[x][y].remove(obj_type)
        self.remove_perceptions(x, y, obj_type)

        self.board[new_x][new_y].append(obj_type)

        if obj_type == "W":
            self.wumpus_pos = new_pos
        elif obj_type == "O":
            self.pits.remove(old_pos)
            self.pits.append(new_pos)

        self.add_perceptions(new_x, new_y, obj_type)

    def remove_perceptions(self, x: int, y: int, obj_type: str):
        """
        Elimina las percepciones de brisa y hedor en las celdas adyacentes a los pozos y al Wumpus.

        Args:
            x (int): Coordenada x de la celda.
            y (int): Coordenada y de la celda.
            obj_type (str): Tipo de objeto a mover (Wumpus o pozo).
        """
        perception = "s" if obj_type == "W" else "b"
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if perception in self.board[nx][ny]:
                    self.board[nx][ny].remove(perception)
                    if perception == "b" and "O" in self.board[nx][ny]:
                        self.board[nx][ny].append("b")
                    if perception == "s" and "W" in self.board[nx][ny]:
                        self.board[nx][ny].append("s")

    def add_perceptions(self, x: int, y: int, obj_type: str):
        """
        Coloca las percepciones de brisa y hedor en las celdas adyacentes a los pozos y al Wumpus.

        Args:
            x (int): Coordenada x de la celda.
            y (int): Coordenada y de la celda.
            obj_type (str): Tipo de objeto a mover (Wumpus o pozo).
        """
        perception = "s" if obj_type == "W" else "b"
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if perception not in self.board[nx][ny]:
                    self.board[nx][ny].append(perception)

    def get_possible_moves(self, pos: tuple):
        """
        Devuelve los movimientos posibles para un objeto en una posición dada.

        Args:
            pos (tuple): Posición actual del objeto.

        Returns:
            list: Lista de movimientos posibles.
        """
        x, y = pos
        moves = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.size
                and 0 <= ny < self.size
                and "W" not in self.board[nx][ny]
                and "O" not in self.board[nx][ny]
                and "G" not in self.board[nx][ny]
            ):
                moves.append((nx, ny))
        return moves
