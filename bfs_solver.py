import logging
import os
import time
from collections import deque

# Create a directory for logs if it doesn't exist
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging configuration to log to a file
logging.basicConfig(
    filename=os.path.join(log_directory, 'bfs_log.txt'),
    filemode='w',
    level=logging.INFO,
    format='%(message)s'
)

# Class representing each cell in the grid
class Cell:
    def __init__(self, x, y, reachable):
        self.x = x
        self.y = y
        self.reachable = reachable
        self.parent = None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

# BFS algorithm implementation
class BFS:
    def __init__(self, width=6, height=6):
        self.grid_width = width
        self.grid_height = height
        self.cells = []
        self.obstacles = []
        self.num_obstacles_to_remove = 0

    def init_grid(self, input_file):
        logging.info(f"Initializing grid from file: {input_file}")
        try:
            with open(input_file, 'r') as file:
                # Read grid dimensions
                dimensions = file.readline().strip()
                self.grid_width, self.grid_height = map(int, dimensions.split())
                
                # Read obstacle positions and the number of obstacles to remove
                for line in file:
                    line = line.strip()
                    
                    # Check if line contains obstacle coordinates
                    if " " in line and "Obstacle" not in line:
                        x, y = map(int, line.split())
                        self.obstacles.append((x, y))
                    
                    # Check for "Obstacle to remove" line and extract the number
                    elif "Obstacle to remove" in line:
                        self.num_obstacles_to_remove = int(line.split('=')[1].strip())
                        break  # Exit loop after reading this line
                
                # Initialize cells with reachability based on obstacles
                for x in range(self.grid_width):
                    for y in range(self.grid_height):
                        reachable = (x, y) not in self.obstacles
                        self.cells.append(Cell(x, y, reachable))

                # Set start and end points
                self.start = self.get_cell(0, 0)
                self.end = self.get_cell(self.grid_width - 1, self.grid_height - 1)
                logging.info(f"Grid initialized: {self.grid_width}x{self.grid_height} with obstacles at {self.obstacles}")
        
        except ValueError as e:
            logging.error(f"Error parsing input file {input_file}: {e}")
            print("Invalid input format! Ensure dimensions and obstacles are formatted correctly in the input file.")
        except FileNotFoundError:
            logging.error(f"Input file {input_file} not found.")
            print(f"Error: Input file '{input_file}' not found.")
        except Exception as e:
            logging.error(f"Unexpected error while initializing grid: {e}")
            print("An unexpected error occurred while initializing the grid.")

    def remove_obstacles(self, num_obstacles):
        removed_obstacles = []
        try:
            for _ in range(min(num_obstacles, len(self.obstacles))):
                obstacle = self.obstacles.pop()
                self.get_cell(obstacle[0], obstacle[1]).reachable = True
                removed_obstacles.append(obstacle)
            logging.info(f"Removed {len(removed_obstacles)} obstacles, new reachable cells: {removed_obstacles}")
        except Exception as e:
            logging.error(f"Error while removing obstacles: {e}")
            print("An error occurred during obstacle removal.")
        return removed_obstacles

    def find_path(self):
        try:
            start_time = time.time()
            logging.info("Starting BFS search algorithm without obstacle removal...")
            path_without_removal = self.process()
            
            if path_without_removal == "No solution":
                logging.info("No solution found without obstacle removal.")

            removed_obstacles = self.remove_obstacles(self.num_obstacles_to_remove)
            logging.info("Re-running BFS after obstacle removal...")
            
            self.reset_grid()
            path_with_removal = self.process()
            
            end_time = time.time()
            time_taken = end_time - start_time
            logging.info(f"Time taken for pathfinding: {time_taken:.4f} seconds")

            if path_with_removal == "No solution":
                print("No solution is found! We need to eliminate more obstacles to find such a walk.")
                logging.info("No solution found after obstacle removal.")
                return

            # Display the results in the specified format
            self.display_results(path_without_removal, path_with_removal, removed_obstacles)

        except Exception as e:
            logging.error(f"Error while finding path: {e}")
            print("An error occurred during pathfinding.")

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def reset_grid(self):
        for cell in self.cells:
            cell.parent = None

    def process(self):
        queue = deque([(self.start, [])])
        visited = set([self.start])

        while queue:
            current, path = queue.popleft()
            new_path = path + [(current.x, current.y)]

            if current == self.end:
                return " -> ".join(f"({x},{y})" for x, y in new_path)

            for neighbor in self.get_adjacent_cells(current):
                if neighbor.reachable and neighbor not in visited:
                    neighbor.parent = current
                    queue.append((neighbor, new_path))
                    visited.add(neighbor)

        return "No solution"

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.grid_height - 1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        return cells

    def display_results(self, path_without_removal, path_with_removal, removed_obstacles):
        print("\n-- The shortest path without eliminating any obstacles --\n")
        if path_without_removal != "No solution":
            print(f"1- The shortest path without eliminating any obstacles is {len(path_without_removal.split(' -> ')) - 1}.")
            print(f"Such path is {path_without_removal}\n")
        else:
            print("No solution is found without eliminating any obstacles.")

        print("\n-- The shortest path with eliminating obstacles --\n")
        if path_with_removal != "No solution":
            print(f"2- The shortest path with removal of {self.num_obstacles_to_remove} obstacle(s) at positions {removed_obstacles} is {len(path_with_removal.split(' -> ')) - 1}.")
            print(f"Such path is {path_with_removal}\n")
        else:
            print("No solution is found after eliminating obstacles.")


# Main program execution
def main():
    input_file = 'dungeon_input.txt'
    bfs = BFS()
    bfs.init_grid(input_file)

    print("\n--The shortest path without eliminating any obstacles--\n")
    logging.info("Attempt to find the shortest path without removing any obstacles.")
    path_without_removal = bfs.process()
    if path_without_removal != "No solution":
        original_path_length = len(path_without_removal.split(" -> "))
        print(f"1- The shortest path without eliminating any obstacles is {original_path_length - 1}.")
        print(f"Such path is {path_without_removal}\n")
    else:
        print("No solution is found! You may need to eliminate more obstacles to find such a walk.")

    # Attempt to remove specified number of obstacles and find the shortest path
    print("\n--The shortest path with eliminating obstacles--\n")
    if bfs.num_obstacles_to_remove > 0:
        logging.info(f"Attempt to remove {bfs.num_obstacles_to_remove} obstacle(s).")
        
        removed_obstacles = bfs.remove_obstacles(bfs.num_obstacles_to_remove)
        if removed_obstacles:
            bfs.reset_grid()
            logging.info(f"Removed obstacles at {removed_obstacles}. Attempting to find the new shortest path.")
            path_with_removal = bfs.process()

            if path_with_removal != "No solution":
                new_path_length = len(path_with_removal.split(" -> "))
                print(f"2- The shortest path with removal of {bfs.num_obstacles_to_remove} obstacle(s) at positions {removed_obstacles} is {new_path_length - 1}.")
                print(f"Such path is {path_with_removal}\n")
            else:
                print("No solution is found after removing obstacles. You may need to eliminate more obstacles to find such a walk.")
        else:
            print("No suitable obstacles to remove.")
    else:
        print("No obstacles specified for removal in the input file.")

    # Optionally prompt user to remove additional obstacles
    while True:
        if not bfs.obstacles:
            print("\nNo more obstacles left to remove.\n")
            break

        user_input = input("Do you want to remove more obstacles? (yes/no): ").strip().lower()
        if user_input == 'yes':
            try:
                obstacles_to_remove = int(input(f"How many obstacles do you want to remove (max {len(bfs.obstacles)})? "))
                if obstacles_to_remove > len(bfs.obstacles):
                    print(f"Cannot remove more than {len(bfs.obstacles)} obstacles.")
                    continue
                
                logging.info(f"User requested to remove {obstacles_to_remove} additional obstacles.")
                additional_removed_obstacles = bfs.remove_obstacles(obstacles_to_remove)
                if additional_removed_obstacles:
                    bfs.reset_grid()
                    path_after_additional_removal = bfs.process()
                    if path_after_additional_removal != "No solution":
                        new_path_length = len(path_after_additional_removal.split(" -> "))
                        print(f"\nThe shortest path after removing {obstacles_to_remove} additional obstacle(s) at {additional_removed_obstacles} is {new_path_length - 1}.")
                        print(f"Such path is {path_after_additional_removal}")
                    else:
                        print("No path found after removing the additional obstacles.")
                else:
                    print("No suitable obstacles to remove.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("*** Thank you! ***")
            break


if __name__ == "__main__":
    main()
