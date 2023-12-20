import random
from sudoku import Sudoku

def generate_sudoku(size, filled_cells):
   # Apenas sudoku quadrados
    puzzle = Sudoku(height=size, width=size, difficulty=filled_cells/(size*size))
    return puzzle.board

def fill_diagonal(grid, row, col):
    nums = list(range(1, len(grid) + 1))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            grid[row + i][col + j] = nums.pop()


def remove_cells(grid, filled_cells):
    cells_to_remove = len(grid) ** 2 - filled_cells
    while cells_to_remove > 0:
        row, col = random.randint(0, len(grid) - 1), random.randint(0, len(grid) - 1)
        if grid[row][col] != 0:
            grid[row][col] = 0
            cells_to_remove -= 1

# Example usage:
size = 9  # Change this for different grid sizes (e.g., 4x4, 6x6, etc.)
filled_cells = 23  # Adjust the number of pre-filled cells as desired
sudoku_grid = generate_sudoku(size, filled_cells)

# Print the generated Sudoku grid
for row in sudoku_grid:
    print(row)
