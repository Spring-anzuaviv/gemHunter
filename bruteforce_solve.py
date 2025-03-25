
# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Bruteforce

def is_valid(KB, case, bit_masks):
    # Có chứa một clause nào mà không thoả mãn thì trả về False
    # Clause không thoả mãn khi tất cả các literal đều False
    for clause in KB:
        is_clause_true = False
        for literal in clause:
            # Nếu từ KB yêu cầu biến True
            if literal > 0 and case & bit_masks[literal]: # Case này gán True thì clause True
                is_clause_true = True
                break  
            # Nếu từ KB yêu cầu biến False
            elif literal < 0 and not case & bit_masks[-literal]: # Case này gán False thì clause True
                is_clause_true = True
                break 
        if not is_clause_true:
            return False
    return True

# Giải bằng bruteforce
def solve_by_bruteforce(KB, empties, numbers):

    # Tạo tất cả các trường hợp có thể của các biến chưa biết
    # => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    length = len(empties)

    # Để tối ưu performance, ta sẽ tăng cường sử dụng hash map và bitwise
    empties_list = list(empties)
    bit_masks = {empties_list[i]: 1 << i for i in range(length)}

    # Tính tổng số lượng bẫy ghi trong các số
    sum_numbers = sum([numbers[pos] for pos in numbers.keys()])
    sum_div_8 = sum_numbers // 8
    
    # sum_số / 8 <= số traps <= min(sum_số, số ô trống)
    min_traps = sum_numbers // 8
    max_traps = min(sum_numbers, length)
    end = 1 << length

    # Bruteforce 2^length trường hợp
    start = (1 << min_traps) - 1
    end = 1 << length
    print(f" - Bruteforcing {end} cases for {length} empty cells...")
    for c in range(start, end):

        # Breakpoints để theo dõi: 2^20-1 = 1048575, 2^24-1 = 16777215, 2^27-1 = 134217727
        if c & 16777215 == 0: print(f"  + Processing case no. {c}...")

        # Nếu num_traps < sum_số/8 thì bỏ qua
        # if c < c.bit_count() < sum_div_8:
        #     continue

        # # Kiểm tra xem trường hợp này có phải là trường hợp đúng không
        if is_valid(KB, c, bit_masks):
            case = [bool(c & (1 << i)) for i in range(length)]
            model = [empties_list[i] if case[i] else -empties_list[i] for i in range(length)]
            return model
    
    return None




    # CÁCH NÀY TƯỞNG NHANH, NHƯNG KHÁ CHẬM.
    # VÍ DỤ: đáp án tại case 3 tỉ, thì với bruteforce như trên, cần loop từ 1 đến 3 tỉ.
    # Còn với cách dưới, loop theo số lượng traps, và tổng số case xét là tổng sigma của comb(n, k) với k từ min_traps đến max_traps
   
    # from math import comb

    # def next_set_of_n_elements(x):
    #     if x == 0: return 0
    #     smallest = x & -x
    #     ripple = x + smallest
    #     new_smallest = ripple & -ripple
    #     ones = ((new_smallest // smallest) >> 1) - 1
    #     return ripple | ones

    # # Bruteforce từ min_traps cho đến max_traps
    # print(f"Bruteforcing {min_traps} - {max_traps} traps / {length} empty cells...")

    # for num_traps in range(min_traps, max_traps + 1):

    #     num_cases = comb(length, num_traps)
    #     print(f"- Processing {num_traps} traps: {num_cases} cases...")

    #     start = (1 << num_traps) - 1
    #     case = start
        
    #     # Breakpoints để theo dõi: 2^20-1 = 1048575, 2^24-1 = 16777215, 2^27-1 = 134217727    
    #     break_point = 1048575 if num_cases <= 2e7 else 16777215 if num_cases <= 2e8 else 134217727
        
    #     # Duyệt qua tất cả các trường hợp có số traps = num_traps
    #     for count in range(1, num_cases + 1):

    #         if count & break_point == 0: print(f"  + Loop no. {count}...")
            
    #         # Kiểm tra xem trường hợp này có phải là trường hợp đúng không
    #         if is_valid(KB, case, bit_masks):
    #             model = [empties_list[i] if case & (1 << i) else -empties_list[i] for i in range(length)]
    #             return model
            
    #         # Tìm trường hợp tiếp theo: thuật toán bit-twiddling hack from hackersdelight.org.
    #         case = next_set_of_n_elements(case)

    # return None
                
