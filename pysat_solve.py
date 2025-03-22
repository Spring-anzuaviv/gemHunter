from pysat.solvers import Solver

def solve_SAT_byPysat(KB):
    solver = Solver(name='m22', bootstrap_with=KB) 
    
    if solver.solve():
        model = solver.get_model()
    else: 
        None

    solver.delete()
    return model