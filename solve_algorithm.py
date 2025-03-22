from generateCNF_automatic import generate_CNF
from utility import add_padding, pos_to_var
from readfile import *
from pysat_solve import *
import timeit

class LogData:
    def __init__(self, algorithm, num_CNF, num_empties, measured_time=None):
        self.algorithm = algorithm
        self.num_CNF = num_CNF
        self.num_empties = num_empties
        self.measured_time = measured_time
        self.traps = 0

def gem_hunter_solver(grid, algorithm='pysat', measure_time=False):
    KB = generate_CNF(grid)
    KB_reserved = [clause.copy() for clause in KB]
    
    grid = add_padding(grid)
    rows = len(grid)
    cols = len(grid[0])
    empties = list()
    numbers = {}

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            cell_value = grid[i][j]
            if cell_value is None:
                empties.append(pos_to_var(i - 1, j - 1, cols - 2))
            elif isinstance(cell_value, int):
                numbers[(i - 1, j - 1)] = cell_value
    
    solver_methods = {
        "pysat": (solve_SAT_byPysat, [KB]),
        # "backtracking": (solve_by_backtracking, [KB, empties]),
        # "bruteforce": (solve_by_bruteforce, [KB, empties, numbers])
    }
    func, args = solver_methods.get(algorithm, (None, None))  
    start = timeit.default_timer() if measure_time else None      

    model = func(*args) if func else None

    measured_time = (timeit.default_timer() - start) * 1000 if measure_time and start is not None else None
    log_data = LogData(algorithm, len(KB), len(empties), measured_time)

    if model is not None:
        set_empties = set(empties)
        model = [x for x in model if x in empties or -x in empties]
        set_model = set(model)
        missing = {-empty for empty in set_empties if empty not in set_model and -empty not in set_model}
        
        model.extend(missing)  # Thêm vào model
        model.sort(key=abs)  # Sắp xếp theo giá trị tuyệt đối
        
        log_data.traps = sum(x > 0 for x in model)
        return model, log_data, KB_reserved

    return None, log_data, KB_reserved

#test
grid = readfile(INPUT_0)
solution, log_info, KB = gem_hunter_solver(grid, measure_time=True)
#solution, log_info, KB, time = solve(grid, measure_time=True)
print("Solution:", solution)
print("Time taken:", log_info.measured_time, "ms")