from itertools import combinations
import os
testcases_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Testcases'))

testcases = {
    "INPUT_0": os.path.join(testcases_dir, "input_0.txt"),
    "INPUT_1": os.path.join(testcases_dir, "input_1.txt"),
    "INPUT_2": os.path.join(testcases_dir, "input_2.txt"),
    "INPUT_3": os.path.join(testcases_dir, "input_3.txt"),
    "OUTPUT_0": os.path.join(testcases_dir, "output_0.txt"),
    "OUTPUT_1": os.path.join(testcases_dir, "output_1.txt"),
    "OUTPUT_2": os.path.join(testcases_dir, "output_2.txt"),
    "OUTPUT_3":  os.path.join(testcases_dir, "output_3.txt"),
}


#1
def add_padding(grid, pad_char = "*"):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    padding_grid = [[pad_char] * (cols + 2)]
    for row in grid:
        padding_grid.append([pad_char] + row + [pad_char])
    padding_grid.append([pad_char] * (cols + 2))

    return padding_grid

#2
def get_neighbors(grid, pos, condition=None):
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    r, c = pos
    directions = [(-1, 0), (1,0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols: 
            if condition is None or condition(grid[nr][nc]):
                neighbors.append([nr, nc])

    return neighbors

#3
def pos_to_var(x: int, y: int, cols) -> int:
    return x * cols + y + 1

#4
def subsets_of(arr, k):
    arr.sort()
    return [list(subset) for subset in combinations(arr, k)]

#5
def result_grid(grid, model):
    if model is None:
        return None
    
    n_row = len(grid)
    n_col = len(grid[0])

    for row in range (n_row):
        for col in range (n_col):
            if grid[row][col] is None:
                idx = pos_to_var(row, col, n_col);
                if idx in model:
                    grid[row][col] = "T"
                else: 
                    grid[row][col] = "G"
    return grid
