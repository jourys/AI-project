import pygame
import sys
import math
from queue import PriorityQueue
from queue import Queue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Visualisation")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    path = []
    # Start with the current node (which should be the end node when this function is called)
    while current in came_from:
        path.append(current)
        current = came_from[current]
        current.make_path()
        draw()
    # Reverse the path to start from the beginning (the start node will be added separately if needed)
    path.reverse()
    return path



def astar_algorithm(draw, grid, start, end):
    print("--- Starting A* algorithm ---\n")
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, current, draw)
            path.insert(0, start)  # Include start in the path
            path_length = len(path) - 1  # Since path includes start and end
            print("The visualized grid shows the explored nodes and the final path.\n")
            print(f"The shortest path is {path_length}. Such path is: " +
                  " -> ".join(f"({spot.row}, {spot.col})" for spot in path))
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    print("No solution is found! We need to eliminate more obstacles to find such a walk.")
    return False

def bfs_algorithm(draw, grid, start, end):
    print("--- Starting BFS algorithm ---\n")
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

        if current == end:
            path = reconstruct_path(came_from, current, draw)
            path.insert(0, start)  # Include start in the path
            path_length = len(path) - 1  # Since path includes start and end
            print("The visualized grid shows the explored nodes and the final path.\n")
            print(f"The shortest path is {path_length}. Such path is: " +
                  " -> ".join(f"({spot.row}, {spot.col})" for spot in path))
            return True

        for neighbor in current.neighbors:
            if not visited[neighbor] and not neighbor.is_barrier():
                came_from[neighbor] = current
                visited[neighbor] = True
                queue.put(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    print("No solution is found! We need to eliminate more obstacles to find such a walk.")
    return False

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_text(win, text, position, size=20, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    win.blit(text_surface, position)

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
    if len(sys.argv) > 2:
        rows = int(sys.argv[1])  # Read the grid size from command line
        algorithm = sys.argv[2]  # Read the algorithm choice from command line
    else:
        rows = 10  # Default size
        algorithm = "bfs"  # Default algorithm

    win = pygame.display.set_mode((width, width))
    grid = make_grid(rows, width)
   
    # Initialize the start node at the top-left corner of the grid
    start = grid[0][0]
    start.make_start()
    # Initialize the end node at the bottom-right corner of the grid
    end = grid[rows-1][rows-1]
    end.make_end()
    run = True

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

             # Allow the user to place barriers with left mouse clicks
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if spot != start and spot != end:
                    spot.make_barrier()

            # Allow the user to reset spots with right mouse clicks
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if spot != start and spot != end:
                    spot.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    if algorithm == "bfs":
                        bfs_algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
                    elif algorithm == "astar":
                        astar_algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    # Reset grid but maintain start and end nodes
                    for row in grid:
                        for spot in row:
                            if spot != start and spot != end:
                                spot.reset()

    pygame.quit()

if __name__ == "__main__":
    WIDTH = 800
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    main(WIN, WIDTH)
