import os
testcases_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Testcases'))

INPUT_0 = os.path.join(testcases_dir, 'input_0.txt')
INPUT_1 = os.path.join(testcases_dir, 'input_1.txt')
INPUT_2 = os.path.join(testcases_dir, 'input_2.txt')
INPUT_3 = os.path.join(testcases_dir, 'input_3.txt')


def readfile(filePath):
    grid = []
    with open(filePath, 'r') as file:
        for line in file:
            row = []
            data = line.strip().split(",")
            for x in data:
                if(x == "_"):
                    row.append(None)
                # elif(x == "T"):
                #     row.append("T")
                # elif(x == "G"):
                #     row.append("G")
                elif x.isnumeric():
                    x = int(x)
                    if x < 0 or x > 8:
                        raise ValueError("Invalid")
                    row.append(x)
                else: raise ValueError("Invalid")
            grid.append(row)
    return grid

