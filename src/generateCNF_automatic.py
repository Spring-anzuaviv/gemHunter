from readfile import *
from utility import *

def generate_clauses(cells, trap_count):
    clauses = []
    n = len(cells)
    
    if len(cells) >= trap_count:
        for subset in subsets_of(cells, n - trap_count + 1):
            clauses.append(subset)
    if trap_count >= 0:
        for subset in subsets_of(cells, trap_count + 1):
            clauses.append([-cell for cell in subset])

    return clauses

def generate_CNF(grid):
    grid = add_padding(grid)
    rows = len(grid)
    cols = len(grid[0])
    cnf = []

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            cell_value = grid[i][j]
            #nếu ô chứa 1 số nguyên
            if isinstance(cell_value, int):
                traps = get_neighbors(grid, [i, j], lambda x: x == "T")

                #số lượng trap cần tìm trong ô chưa biết
                trap_count = cell_value - len(traps)

                unknowns = get_neighbors(grid, [i, j], lambda x: x is None)
                #chuyển vị trí 2D của các ô chưa biết thành chỉ số 1D (bắt đầu từ 1)
                unknowns_1D = [pos_to_var(pos[0] - 1, pos[1] - 1, cols - 2) for pos in unknowns]

                #tạo clauses nếu còn trap cần xđ
                if 0 <= trap_count <= len(unknowns_1D):
                    cnf.extend(generate_clauses(unknowns_1D, trap_count))
    cnf = [list(clause) for clause in sorted({tuple(sorted(clause)) for clause in cnf}, key=lambda x: (len(x), x))]
    return cnf