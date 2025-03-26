def is_valid(KB, model_dict):
    """ Kiểm tra nếu model hiện tại thỏa mãn KB """
    for clause in KB:
        clause_satisfied = False
        for literal in clause:
            if model_dict.get(abs(literal), False) == (literal > 0):
                clause_satisfied = True
                break
        if not clause_satisfied:
                return False
    return True

def solve_by_bruteforce(KB, empties, numbers):
    empties_list = list(empties)
    
    sum_numbers = sum(numbers.values())
    min_traps = sum_numbers // 8
    max_traps = min(sum_numbers, len(empties))

    print(f" - Bruteforcing {2**len(empties)} cases for {len(empties)} empty cells...")

    def recursive_bruteforce(index, model_dict, num_traps):
        if index == len(empties_list):
            # Kiểm tra nghiệm
            if is_valid(KB, model_dict):
                solution = []
                for var in empties_list:
                    if model_dict[var]:  
                        solution.append(var)   # Biến có giá trị True
                    else:
                        solution.append(-var)  # Biến có giá trị False
                return solution  # Trả về nghiệm hợp lệ
            return None

        var = empties_list[index]  # Lấy biến hiện tại

        # Nếu số traps vượt quá giới hạn, dừng lại
        if num_traps > max_traps:
            return None
        
        # Thử gán biến hiện tại là False (G)
        model_dict[var] = False
        result = recursive_bruteforce(index + 1, model_dict, num_traps)
        if result:
            return result

        # Thử gán biến hiện tại là True (T) => tăng số traps
        model_dict[var] = True
        result = recursive_bruteforce(index + 1, model_dict, num_traps + 1)
        if result:
            return result
        
        del model_dict[var]
        return None

    return recursive_bruteforce(0, {}, 0)
