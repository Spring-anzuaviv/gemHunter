from itertools import combinations

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

