from collections import Counter
from copy import deepcopy

def solve_by_backtracking(KB, empties):

    def checking_cnf(KB, model):
        for clause in KB:
            clause_satisfied = False 
            for literal in clause:
                if literal in model:
                    clause_satisfied = True  
                    break 
            if not clause_satisfied:
                return False
        # Nếu tất cả các clause đều thỏa mãn, trả về True
        return True

    def unit_propagation(KB, model):
        while True:
            unit_clauses = []  # Danh sách chứa các mệnh đề đơn

            for clause in KB:
                if len(clause) == 1:  # Nếu mệnh đề chỉ chứa một literal
                    unit_clauses.append(clause[0])

            if not unit_clauses:
                break
            
            for unit in unit_clauses:
                if -unit in model:
                    return None  
                if unit not in model:  
                    model.append(unit)

                new_KB = []
                for clause in KB:
                    if unit not in clause:
                        new_KB.append(clause)
                KB = new_KB

                for clause in KB:
                    if -unit in clause:
                        clause.remove(-unit)
        
        return KB, model

    def pure_literal_elimination(KB, model):
        literals = set()
        for clause in KB:
            for lit in clause:
                literals.add(lit)
        
        pure_literals = set()
        for lit in literals:
            if -lit not in literals:  # Nếu không tồn tại literal đối nghịch (-lit)
                pure_literals.add(lit)

        if not pure_literals:
            return KB, model

        for lit in pure_literals:
            if lit not in model: 
                model.append(lit)

        new_KB = []
        for clause in KB:
            has_pure_literal = False  # Kiểm tra xem có pure literal trong clause không
            for lit in clause:
                if lit in pure_literals:  # Nếu clause chứa một pure literal
                    has_pure_literal = True
                    break  # Không cần kiểm tra tiếp, bỏ clause này
            
            if not has_pure_literal:
                new_KB.append(clause)  # Giữ lại clause nếu không chứa pure literal

        KB = new_KB
        return KB, model

    # **Chọn biến thông minh hơn**: Biến xuất hiện nhiều nhất trong KB:
    def choose_best_variable(KB):
        counter = Counter()
        for clause in KB:
            for lit in clause:
                counter[abs(lit)] += 1

        return max(counter, key=counter.get) if counter else None

    def backtracking_util(KB, model):
        KB, model = unit_propagation(KB, model)
        if KB is None:
            return None

        KB, model = pure_literal_elimination(KB, model)
        if not KB:
            return model if checking_cnf(KB, model) else None

        var = choose_best_variable(KB)
        if var is None:
            return None

        # Thử gán True trước
        result = backtracking_util([clause.copy() for clause in KB], deepcopy(model) + [var])
        if result is not None:
            return result

        # Nếu thất bại, thử gán False
        result = backtracking_util([clause.copy() for clause in KB], deepcopy(model) + [-var])
        return result

    return backtracking_util(KB, [])
