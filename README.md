# Rescuing the Princess: A Search Algorithm Project

## Overview
This project implements search algorithms to navigate a dungeon and rescue Princess P from the clutches of evil. The dungeon is represented as a grid, where obstacles ('X') and empty cells ('.') affect the knight's journey from the starting point (0, 0) to the goal (M-1, N-1).

## Objectives
- Implement two search algorithms: A* (informed) and BFS (uninformed).
- Allow for the removal of obstacles to analyze the impact on path length.
- Visualize the search process to demonstrate the knight's movement. (ongoing development)

## Files
- `A*_solver.py`: Implements the A* search algorithm.
- `bfs_solver.py`: Implements the BFS search algorithm.
- `input.txt`: Input file includes the dimensions of the dungeon grid (M x N) and coordinates of obstacles, as well as the number of obstacles to be removed (optional).
- `game_ui.py`: Contains the user interface for visualizing the game.
- `welcome_ui.py`: Displays the welcome screen.

## Usage
1. Run `welcome_ui.py` to see the welcome screen.
2. Press the "Start" button to access the user interface in `game_ui.py`.
3. Choose the input file and select the algorithm you want to run.

## Conclusion
This project is designed for the SWE485 course at King Saud University. It aims to enhance understanding of search algorithms and their application in real-world scenarios.
