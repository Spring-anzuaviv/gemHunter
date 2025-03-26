def readfile(filePath):
    grid = []
    with open(filePath, 'r') as file:
        for line in file:
            row = []
            data = line.strip().split(",")
            for x in data:
                if(x == "_"):
                    row.append(None)
                elif x.isnumeric():
                    x = int(x)
                    if x < 0 or x > 8:
                        raise ValueError("Invalid")
                    row.append(x)
                else: raise ValueError("Invalid")
            grid.append(row)
    return grid

def writefile(filePath, grid):
    with open(filePath, 'w') as file:
        for row in grid:
            line = ",".join(map(str, row))
            file.write(line + "\n")