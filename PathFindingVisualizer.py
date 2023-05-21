import logging
from logging.config import dictConfig
import pygame
from queue import PriorityQueue

"""
This project lacks a UI. 
To quickly begin, run the code and LEFT-CLICK on any 2 squarse on the grid.
Then create some barriers by DRAGGING THE MOUSE BUTTON over the white squares.
To initialize, press SPACE-BAR.
Then RESET by pressing / .

Controls are hence stated:
1. The FIRST LEFT-CLICK will produce the START position.
2. SECOND LEFT-CLICK will produce the END position.
3. ANY LEFT-CLICKS or DRAG hence-forth will produce BARRIERS.
4. To ERASE, RIGHT-CLICK or DRAG RIGHT-CLICK. 
5. To INITIALIZE ALGORITHM, press SPACEBAR.
6. To RESET BOARD, press the FORWARD-SLASH key (/).

"""


def setup_logging():
    fmt = '%(asctime)s | %(threadName)s - %(levelname)s - %(filename)s - %(lineno)s - func=%(funcName)s : "%(message)s"'
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters':
            {
                'standard':
                    {
                        'format': fmt
                    }
            },
        'handlers':
            {
                'default':
                    {
                        'class': 'logging.StreamHandler',
                        'formatter': 'standard',
                        'level': 'DEBUG',
                        'stream': 'ext://sys.stdout'
                    },
            },
        'loggers':
            {
                'logger':
                    {
                        'handlers': ['default'],
                        'level': 'DEBUG',
                        'propagate': False
                    }
            }
    }

    logging.config.dictConfig(logging_config)


setup_logging()
log = logging.getLogger('logger')

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path-Finding Algorithm Representation")


AQUA = (0, 0, 205)
FOLIAGE = (0, 201, 87)
ROAD = (255, 185, 15)
GREY = (156, 156, 156)
RED = (220, 20, 60)
VIOLET = (138, 43, 226)
WHITE = (248, 248, 255)
ORANGE = (255, 125, 64)
BLACK = (41, 36, 33)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

        self.neighbors = []

    def __lt__(self, other):
        return False

    def set_pos(self, row, col):
        self.row = row
        self.col = col

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = FOLIAGE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = VIOLET

    def make_end(self):
        self.color = ORANGE

    def make_path(self):
        self.color = ROAD

    def reset(self):
        self.color = WHITE

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == FOLIAGE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == VIOLET

    def is_path(self):
        return self.color == ROAD

    def is_end(self):
        return self.color == ORANGE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])  # DOWN

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])  # UP

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])  # RIGHT

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])  # LEFT


class RectGrid(list):
    def __init__(self, win, width, rows_cols):
        super().__init__()
        self.win = win
        self.width = width
        self.rows_cols = rows_cols
        self.node_width = self.width // self.rows_cols

    def initialize_grid(self):
        """
        Each row on the grid is represented by a list, within which the Nodes are
        encapsulated by order of row-column.
        """
        for row in range(self.rows_cols):
            self.append([])
            for col in range(self.rows_cols):
                self[row].append(Node(row, col, self.node_width, self.rows_cols))

    def draw_grid(self):
        for row in range(self.rows_cols):
            pygame.draw.line(self.win, BLACK, (0, row * self.node_width), (self.width, row * self.node_width))
        for col in range(self.rows_cols):
            pygame.draw.line(self.win, BLACK, (col * self.node_width, 0), (col * self.node_width, self.width))

    def draw_screen(self):
        self.win.fill(WHITE)
        for row in self:
            for node in row:
                node.draw(self.win)
        self.draw_grid()
        pygame.display.update()

    def get_clicked_pos(self, mouse_pos):
        mouse_y, mouse_x = mouse_pos
        row = mouse_y // self.node_width
        col = mouse_x // self.node_width

        return row, col


def heuristic(p1, p2):
    """
    Returns the L-distance (Manhattan Distance) between 2 given points.

    .
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def algorithm(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            node = came_from[end]
            while node != start:
                node.make_path()
                node = came_from[node]
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        grid.draw_screen()

        if not current.is_start():
            current.make_closed()

    return False


def main(win, width):
    ROWS_COLS = 50
    grid = RectGrid(win, width, ROWS_COLS)
    grid.initialize_grid()

    start = None
    end = None

    run = True
    started = False
    while run:
        grid.draw_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK, DRAW
                mouse_pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(mouse_pos)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    node.make_start()

                elif not end and node != start:
                    end = node
                    node.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK, ERASE
                mouse_pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(mouse_pos)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(grid, start, end)

                if event.key == pygame.K_SLASH:
                    ROWS_COLS = 50
                    grid = RectGrid(win, width, ROWS_COLS)
                    grid.initialize_grid()

                    start = None
                    end = None

                    run = True
                    started = False

    pygame.quit()


main(WIN, WIDTH)

