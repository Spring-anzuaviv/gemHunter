from generateCNF_automatic import generate_CNF
from utility import *
from readfile import *
from bruteforce_solve import *
from backtracking_solve import *
from pysat_solve import *
import timeit

class LogData:
    def __init__(self, algorithm, num_CNF, num_empties, solution, measured_time=None):
        self.algorithm = algorithm
        self.num_CNF = num_CNF
        self.num_empties = num_empties
        self.measured_time = measured_time
        self.model = solution
        self.traps = 0

def gem_hunter_solver(grid, algorithm, measure_time=False):
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
        "backtracking": (solve_by_backtracking, [KB, empties]),
        "bruteforce": (solve_by_bruteforce, [KB, empties, numbers])
    }
    func, args = solver_methods.get(algorithm, (None, None))  
    start = timeit.default_timer() if measure_time else None      

    if func:
        model = func(*args)
    else: 
        model = None
    
    measured_time = (timeit.default_timer() - start) * 1000 if measure_time and start is not None else None
    log_data = LogData(algorithm, len(KB), len(empties), model, measured_time)

    if model is not None:
        set_empties = set(empties)
        model = [x for x in model if x in empties or -x in empties]
        set_model = set(model)
        missing = {-empty for empty in set_empties if empty not in set_model and -empty not in set_model}
        
        model.extend(missing)
        model.sort(key=abs)  # Sắp xếp theo giá trị tuyệt đối
        
        log_data.traps = sum(x > 0 for x in model)
        log_data.model = model
        return log_data, KB_reserved

    return log_data, KB_reserved

def main():
    while True:
        testcase_name = input("Input name of testcase (or enter 'X' to exit): ").strip().upper()
        if testcase_name.upper() == 'X':  # Thoát vòng lặp nếu nhập 'X'
            break   
        
        method_name = input("Input name of method ['pysat', 'bruteforce', 'backtracking']: ").strip().lower()
        testcase_num = "" 
        for char in testcase_name:
            if char.isdigit():
                testcase_num += char
        if testcase_num:
            testcase_num = int(testcase_num)
        else:
            testcase_num = None

        if testcase_name in testcases:
            testcase_path = testcases[testcase_name]
            
            if os.path.exists(testcase_path):
                grid = readfile(testcase_path)
                
                if method_name in ['pysat', 'backtracking', 'bruteforce']:
                    log_data, KB = gem_hunter_solver(grid, method_name, measure_time=True)
                    print(f"Solution {log_data.algorithm}: ", log_data.model)
                    print("Time taken:", log_data.measured_time, "ms")
                else:
                    print("Error: Invalid method. Input again.")
                    continue

                result = result_grid(grid, log_data.model)

                if testcase_num == 0:
                    writefile(testcases["OUTPUT_0"], result)
                elif testcase_num == 1:
                    writefile(testcases["OUTPUT_1"], result)
                elif testcase_num == 2:
                    writefile(testcases["OUTPUT_2"], result)
                elif testcase_num == 3:
                    writefile(testcases["OUTPUT_3"], result)
            else:
                print(f"Error: File '{testcase_path}' no exit.")
        else:
            print(f"Error: Do not find test case '{testcase_name}'. Input again.")
        print("=" * 40 + "\n")

if __name__ == "__main__":
    main()
