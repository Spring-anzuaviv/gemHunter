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
    
    def propagate(KB, assigned_literal):
        """
        Xóa các clause được thỏa mãn bởi assigned_literal
        và xóa literal bù trừ trong các clause còn lại.
        Nếu sinh ra clause rỗng => mâu thuẫn => return None
        """
        new_KB = []
        for clause in KB:
            # Nếu clause chứa assigned_literal, clause này đã được thỏa => bỏ qua
            if assigned_literal in clause:
                continue

            # Nếu clause chứa -assigned_literal, ta phải xóa -assigned_literal
            if -assigned_literal in clause:
                new_clause = [lit for lit in clause if lit != -assigned_literal]
                # Nếu sau khi xóa literal, clause thành rỗng => xung đột
                if len(new_clause) == 0:
                    return None
                new_KB.append(new_clause)
            else:
                # Giữ nguyên clause nếu không liên quan
                new_KB.append(clause)

        return new_KB


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
        if KB is None:
            return None
        if not KB:  # Nếu rỗng => đã thỏa
            return model if checking_cnf(KB, model) else None

        var = choose_best_variable(KB)
        if var is None:
            return None

        # Thử gán True trước
        model_true = deepcopy(model)
        model_true.append(var)
        KB_true = propagate([clause.copy() for clause in KB], var)
        if KB_true is not None:  # propagate không trả về None
            result = backtracking_util(KB_true, model_true)
        if result is not None:
            return result

        # Nếu thất bại, thử gán False
        model_false = deepcopy(model)
        model_false.append(-var)
        KB_false = propagate([clause.copy() for clause in KB], -var)
        if KB_false is not None:
            result = backtracking_util(KB_false, model_false)
        if result is not None:
            return result
        
        return None

    return backtracking_util(KB, [])
