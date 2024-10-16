import random

class Board:
    def __init__(self, size, custom_board=None):
        self.size = size
        self.custom_board = custom_board
        self.reset()

    def reset(self):
        self.board = [[[] for _ in range(self.size)] for _ in range(self.size)]
        self.agent_pos = None
        self.wumpus_pos = None
        self.gold_pos = None
        self.pits = []

        if self.custom_board:
            self.load_custom_board(self.custom_board)
        else:
            self.initialize_board()

    def load_custom_board(self, custom_board):
        for i in range(self.size):
            for j in range(self.size):
                cell_content = custom_board[i][j]
                if isinstance(cell_content, str) and cell_content.startswith('[') and cell_content.endswith(']'):
                    cell_content = cell_content[1:-1]
                
                for char in cell_content:
                    if char == 'A':
                        self.agent_pos = (i, j)
                        self.board[i][j].append('A')
                    elif char == 'W':
                        self.wumpus_pos = (i, j)
                        self.board[i][j].append('W')
                    elif char == 'O':
                        self.pits.append((i, j))
                        self.board[i][j].append('P')
                    elif char == 'G':
                        self.gold_pos = (i, j)
                        self.board[i][j].append('G')
                    elif char == 'b':
                        self.board[i][j].append('b')
                    elif char == 's':
                        self.board[i][j].append('s')
        
        if not self.agent_pos:
            raise ValueError("El tablero personalizado debe contener un agente (A)")
        if not self.gold_pos:
            raise ValueError("El tablero personalizado debe contener oro (G)")

    def initialize_board(self):
        self.place_agent()
        self.place_wumpus()
        self.place_gold()
        self.place_pits()
        self.place_breezes_and_stenches()

    def place_agent(self):
        self.agent_pos = (self.size-1, 0)
        self.board[self.agent_pos[0]][self.agent_pos[1]].append('A')

    def place_wumpus(self):
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x, y) != self.agent_pos and not self.is_adjacent(x, y, self.pits) and len(self.board[x][y]) < 3:
                self.wumpus_pos = (x, y)
                self.board[x][y].append('W')
                break

    def place_gold(self):
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x, y) != self.agent_pos and (x, y) != self.wumpus_pos and len(self.board[x][y]) < 3:
                self.gold_pos = (x, y)
                self.board[x][y].append('G')
                break

    def place_pits(self):
        num_pits = self.size * self.size // 10
        for _ in range(num_pits):
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if (x, y) not in [self.agent_pos, self.wumpus_pos, self.gold_pos] and (x, y) not in self.pits and len(self.board[x][y]) < 3:
                    if not self.is_adjacent(x, y, [self.wumpus_pos]):
                        self.pits.append((x, y))
                        self.board[x][y].append('P')
                        break

    def is_adjacent(self, x, y, positions):
        for pos in positions:
            if pos:
                dx, dy = abs(x - pos[0]), abs(y - pos[1])
                if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                    return True
        return False

    def place_breezes_and_stenches(self):
        for x in range(self.size):
            for y in range(self.size):
                if 'P' in self.board[x][y]:
                    self.place_perception(x, y, 'b')
                elif 'W' in self.board[x][y]:
                    self.place_perception(x, y, 's')

    def place_perception(self, x, y, perception):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if perception not in self.board[nx][ny] and 'P' not in self.board[nx][ny] and 'W' not in self.board[nx][ny]:
                    self.board[nx][ny].append(perception)

    def get_board(self):
        return self.board

    def move_agent(self, direction):
        dx, dy = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }[direction]

        new_x, new_y = self.agent_pos[0] + dx, self.agent_pos[1] + dy

        if 0 <= new_x < self.size and 0 <= new_y < self.size:
            if 'A' in self.board[self.agent_pos[0]][self.agent_pos[1]]:
                self.board[self.agent_pos[0]][self.agent_pos[1]].remove('A')
            self.agent_pos = (new_x, new_y)
            if 'A' not in self.board[new_x][new_y]:
                self.board[new_x][new_y].append('A')
            self.check_perceptions()
            return True
        return False

    def undo_move_agent(self, direction):
        opposite_direction = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }[direction]
        self.move_agent(opposite_direction)

    def check_perceptions(self):
        x, y = self.agent_pos
        perceptions = []
        if 'b' in self.board[x][y]:
            perceptions.append("Sientes una brisa. Debe haber un hoyo cerca.")
        if 's' in self.board[x][y]:
            perceptions.append("Percibes un hedor. El Wumpus debe estar cerca.")
        
        if perceptions:
            print("\n".join(perceptions))

    def shoot_arrow(self, direction):
        dx, dy = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }[direction]

        x, y = self.agent_pos
        while 0 <= x < self.size and 0 <= y < self.size:
            if 'W' in self.board[x][y]:
                self.board[x][y].remove('W')
                self.board[x][y].append('X')  # X represents dead Wumpus
                self.wumpus_pos = None
                return True
            x, y = x + dx, y + dy
        return False

    def check_game_over(self):
        x, y = self.agent_pos
        if 'W' in self.board[x][y]:
            return True, "¡El Wumpus te ha atrapado!"
        if 'P' in self.board[x][y]:
            return True, "¡Has caído en un hoyo!"
        if 'G' in self.board[x][y]:
            return True, "¡Has encontrado el oro! ¡Ganaste!"
        return False, None

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def move_dangerous_object(self):
        objects = [('W', self.wumpus_pos)] + [('P', pit) for pit in self.pits]
        obj_type, obj_pos = random.choice(objects)

        possible_moves = self.get_possible_moves(obj_pos)
        if not possible_moves:
            return False

        new_pos = random.choice(possible_moves)
        self.move_object(obj_type, obj_pos, new_pos)
        return True

    def move_object(self, obj_type, old_pos, new_pos):
        x, y = old_pos
        new_x, new_y = new_pos

        if obj_type in self.board[x][y]:
            self.board[x][y].remove(obj_type)
        self.remove_perceptions(x, y, obj_type)

        self.board[new_x][new_y].append(obj_type)

        if obj_type == 'W':
            self.wumpus_pos = new_pos
        elif obj_type == 'P':
            self.pits.remove(old_pos)
            self.pits.append(new_pos)

        self.add_perceptions(new_x, new_y, obj_type)

    def remove_perceptions(self, x, y, obj_type):
        perception = 's' if obj_type == 'W' else 'b'
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if perception in self.board[nx][ny]:
                    self.board[nx][ny].remove(perception)

    def add_perceptions(self, x, y, obj_type):
        perception = 's' if obj_type == 'W' else 'b'
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if perception not in self.board[nx][ny]:
                    self.board[nx][ny].append(perception)

    def get_possible_moves(self, pos):
        x, y = pos
        moves = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and 'A' not in self.board[nx][ny] and 'G' not in self.board[nx][ny]:
                moves.append((nx, ny))
        return moves