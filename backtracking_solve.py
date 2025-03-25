# # Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Backtracking

# def is_conflict(KB, solution_bits, bits_length, empties_dict, empties_set, bit_masks):
#     # Có chứa một clause nào mà không thoả mãn thì trả về True
#     # Clause không thoả mãn khi tất cả các literal đều False

#     # Empties_dict: {pos: index} với pos là vị trí ô trống, index là index của ô trống trong solution
    
#     for clause in KB:
        
#         is_clause_true = False
#         for literal in clause:
#             # Nếu literal không phải là ô trống thì bỏ qua

#             # Nếu literal là ô trống và chưa tới lượt gán giá trị thì bỏ qua clause
#             index = empties_dict[literal] if literal > 0 else empties_dict[-literal]
#             if index > bits_length:
#                 is_clause_true = True
#                 break

#             # Nếu từ KB yêu cầu biến True
#             if literal > 0 and solution_bits & bit_masks[literal]: # Case này gán True thì clause True
#                 is_clause_true = True
#                 break  
#             # Nếu từ KB yêu cầu biến False
#             elif literal < 0 and not solution_bits & bit_masks[-literal]: # Case này gán False thì clause True
#                 is_clause_true = True
#                 break 

#         if not is_clause_true:
#             return True

#     return False

# # Giải bằng backtracking với DFS: lần lượt gán giá trị cho các ô trống là 0 hoặc 1 (tức là bằng -empties[i] hoặc empties[i]), sau đó kiểm tra xem có conflict không, nếu không thì tiếp tục gán cho ô tiếp theo, nếu có thì quay lui và thử giá trị khác cho ô hiện tại
# def solve_by_backtracking(KB, empties):
    
#     # Để tối ưu performance, ta sẽ tăng cường sử dụng hash map và bitwise
#     length = len(empties)
#     empties_list = list(empties)
#     empties_dict = {empties_list[i]: i for i in range(length)}

#     # bit_masks[n] = 00010 tức n là ô trống thứ 2; c & bit_masks[n] trả về bit thứ 2 của c
#     bit_masks = {empties_list[i]: 1 << i for i in range(length)}

#     # Hàm đệ quy giải bài toán: sử dụng DFS và backtracking
#     def backtrack(solution_bits, index):

#         if index == length:
#             return solution_bits

#         # Gán giá trị cho ô trống là 0
#         solution_bits = solution_bits & ~bit_masks[empties_list[index]]
#         if not is_conflict(KB, solution_bits, index, empties_dict, set(empties_list), bit_masks):
#             result = backtrack(solution_bits, index + 1)
#             if result is not None:
#                 return result                     
        
#         # Gán giá trị cho ô trống là 1
#         solution_bits = solution_bits | bit_masks[empties_list[index]]
#         if not is_conflict(KB, solution_bits, index, empties_dict, set(empties_list), bit_masks):
#             result = backtrack(solution_bits, index + 1)
#             if result is not None:
#                 return result        
            
#         # Nếu không tìm được giá trị thích hợp cho ô trống thứ index thì quay lui
#         return None
    
#     # Bắt đầu giải bài toán
#     solution_bits = backtrack(0, 0)
#     if solution_bits is None:
#         return None
    
#     solution = [bool(solution_bits & (1 << i)) for i in range(length)]
#     model = [empties_list[i] if solution[i] else -empties_list[i] for i in range(length)]
#     return model

from collections import Counter
from copy import deepcopy

def solve_by_backtracking(KB, empties):
    # Kiểm tra nếu model thỏa mãn toàn bộ CNF
    def checking_cnf(KB, model):
        return all(any(lit in model for lit in clause) for clause in KB)

    # Lan truyền unit propagation
    def unit_propagation(KB, model):
        while True:
            unit_clauses = [clause[0] for clause in KB if len(clause) == 1]
            if not unit_clauses:
                break
            
            for unit in unit_clauses:
                if -unit in model:
                    return None  # Xung đột xảy ra
                if unit not in model:  # Kiểm tra trước khi thêm
                    model.append(unit)

                KB = [clause for clause in KB if unit not in clause]
                for clause in KB:
                    if -unit in clause:
                        clause.remove(-unit)
        
        return KB, model

    # Loại bỏ biến thuần túy (pure literal elimination)
    def pure_literal_elimination(KB, model):
        literals = {lit for clause in KB for lit in clause}
        pure_literals = {lit for lit in literals if -lit not in literals}

        if not pure_literals:
            return KB, model

        for lit in pure_literals:
            if lit not in model:  # Kiểm tra trước khi thêm
                model.append(lit)
        #model.extend(pure_literals)
        KB = [clause for clause in KB if not any(lit in pure_literals for lit in clause)]
        return KB, model

    # **Chọn biến thông minh hơn**: Biến xuất hiện nhiều nhất trong KB: đúng
    def choose_best_variable(KB):
        counter = Counter(abs(lit) for clause in KB for lit in clause)
        return max(counter, key=counter.get) if counter else None

    # Hàm backtracking tối ưu
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
