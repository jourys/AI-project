from customtkinter import *
from tkinter import messagebox
import pygame
import sys
from queue import Queue, PriorityQueue

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

pygame.init()

class Spot:
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * height
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols

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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

def make_grid(rows, cols, win_width, win_height):
    grid = []
    cell_width = win_width // cols
    cell_height = win_height // rows
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j, cell_width, cell_height, rows, cols)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, cols, win_width, win_height):
    cell_width = win_width // cols
    cell_height = win_height // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * cell_height), (win_width, i * cell_height))
    for j in range(cols):
        pygame.draw.line(win, GREY, (j * cell_width, 0), (j * cell_width, win_height))

def draw(win, grid, rows, cols, win_width, win_height):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, cols, win_width, win_height)
    pygame.display.update()

def get_clicked_pos(pos, rows, cols, win_width, win_height):
    cell_width = win_width // cols
    cell_height = win_height // rows
    x, y = pos
    row = y // cell_height
    col = x // cell_width
    if row >= rows:
        row = rows - 1
    if col >= cols:
        col = cols - 1
    return row, col

def astar_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    nodes_expanded = 0

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_expanded += 1

        if current == end:
            path_length = reconstruct_path(came_from, end, draw)
            end.make_end()
            messagebox.showinfo("Path Information", f"Nodes Expanded: {nodes_expanded}\nPath Length: {path_length}")
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

    messagebox.showinfo("Path Information", "No path found.")
    return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    path_length = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        path_length += 1
    return path_length

def bfs_algorithm(draw, grid, start, end):
    print("--- Starting BFS algorithm ---\n")
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    nodes_expanded = 0

    while not queue.empty():
        current = queue.get()
        nodes_expanded += 1

        if current == end:
            path_length = reconstruct_path(came_from, current, draw)
            end.make_end()
            messagebox.showinfo("Path Information", f"Nodes Expanded: {nodes_expanded}\nPath Length: {path_length}")
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

    messagebox.showinfo("Path Information", "No path found.")
    return False

def main(win, width, height, rows, cols, algorithm):
    grid = make_grid(rows, cols, width, height)
    start = grid[0][0]
    start.make_start()
    end = grid[rows - 1][cols - 1]
    end.make_end()
    run = True

    while run:
        draw(win, grid, rows, cols, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    if algorithm == "astar":
                        astar_algorithm(lambda: draw(win, grid, rows, cols, width, height), grid, start, end)
                    elif algorithm == "bfs":
                        bfs_algorithm(lambda: draw(win, grid, rows, cols, width, height), grid, start, end)

                if event.key == pygame.K_c:
                    for row in grid:
                        for spot in row:
                            if spot != start and spot != end:
                                spot.reset()

        # Handle mouse clicks outside the event loop
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, rows, cols, width, height)
            spot = grid[row][col]
            if spot != start and spot != end:
                spot.make_barrier()
        elif pygame.mouse.get_pressed()[2]:  # Right mouse button
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, rows, cols, width, height)
            spot = grid[row][col]
            if spot != start and spot != end:
                spot.reset()

    pygame.quit()

def display_welcome_screen():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Valiant Knight - Save The Princess')

    welcome_image = pygame.image.load(r'/Users/lamaalnasser/Documents/GitHub/SWE485/background.png')  # Replace with the path to your image
    welcome_image = pygame.transform.scale(welcome_image, (800, 600))

    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Let's Start", True, (0, 0, 0))
    button_rect = pygame.Rect(300, 450, 200, 70)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    running = True
    while running:
        screen.blit(welcome_image, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    return True

def display_algorithm_gui():
    window = CTk()
    window.title("Rescuing the Princess | Visualizer")
    window.configure(bg="#242424")
    app_width, app_height = 420, 260
    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
    x, y = (screen_width / 2) - (app_width / 2), (screen_height / 2) - (app_height / 2)
    window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    window.resizable(0, 0)

    label1 = CTkLabel(window, text="Algorithm", fg_color="transparent", font=("calibri", 15), text_color="#00FF89")
    label1.place(relx=0.5, rely=0.15, anchor=CENTER)

    choice = StringVar()
    combobox1 = CTkComboBox(window, values=["A* Algorithm", "BFS Algorithm"], variable=choice, state="readonly", button_color="#00FF89")
    combobox1.set("A* Algorithm")
    combobox1.place(relx=0.5, rely=0.30, anchor=CENTER)

    label2 = CTkLabel(window, text="Grid Dimensions (e.g., 10x5)", fg_color="transparent", font=("calibri", 15), text_color="#FF0099")
    label2.place(relx=0.5, rely=0.50, anchor=CENTER)

    gridDimension = StringVar()
    entryGridDimension = CTkEntry(window, textvariable=gridDimension, width=120, placeholder_text="e.g., 10x5")
    entryGridDimension.place(relx=0.5, rely=0.65, anchor=CENTER)

    def parse_grid_dimensions(dim_str):
        parts = dim_str.lower().split('x')
        if len(parts) != 2:
            messagebox.showerror("Invalid Format", "Enter dimensions as 'NxM'.")
            return None
        try:
            rows, cols = map(int, parts)
            if rows <= 0 or cols <= 0:
                raise ValueError("Dimensions must be positive.")
            return rows, cols
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter positive integers.")
            return None

    def runner():
        grid_dims = parse_grid_dimensions(gridDimension.get())
        algorithm_choice = choice.get()
        if grid_dims:
            rows, cols = grid_dims
            if algorithm_choice == "A* Algorithm":
                algorithm = "astar"
            elif algorithm_choice == "BFS Algorithm":
                algorithm = "bfs"
            main(pygame.display.set_mode((WIDTH, HEIGHT)), WIDTH, HEIGHT, rows, cols, algorithm)
        else:
            messagebox.showerror("Error", "Invalid input.")

    submit_button = CTkButton(window, text="Start", command=runner, font=('calibri', 12, 'bold'))
    submit_button.place(relx=0.5, rely=0.85, anchor=CENTER)

    window.mainloop()

def main_gui():
    if display_welcome_screen():
        display_algorithm_gui()

if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600
    main_gui()
