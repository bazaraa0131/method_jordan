from fractions import Fraction

import const as Const

def read(from_input: bool = True, input_path: str | None = None):
    if from_input:
        src = input
        close = lambda: None
    else:
        if input_path is None:
            raise ValueError("input_path must be provided when from_input is False")
        f = open(input_path, "r")
        src = lambda: f.readline().strip()
        close = f.close

    # first line: e v
    e, v = map(int, src().split())

    mat = [[Fraction() for _ in range(v)] for _ in range(e)]
    vec = [Fraction() for _ in range(e)]

    # each line: v coefficients + 1 RHS
    for r in range(e):
        row = list(map(Fraction, src().split()))
        if len(row) != v + 1:
            raise ValueError(f"Expected {v+1} values on line {r+1}, got {len(row)}")
        mat[r] = row[:v]
        vec[r] = row[v]

    close()
    return e, v, mat, vec

class Cell:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value
    def update_type(self, type):
        self.type = type
    def update_value(self, value):
        self.value = value
    def get_type(self):
        return self.type
    def get_value(self):
        return self.value

class Solver:
    def __init__(self, from_input = True, input_path = None):
        e, v, mat, vec = read(from_input, input_path)

        self.e = e
        self.v = v

        self.table = [[Cell() for _ in range(self.v + 1)] for _ in range(e + 1)]

        self.table[0][0].update_value("#")

        for i in range(1, self.v + 1):
            self.table[0][i].update_type(Const.VARIABLE_CELL)
            self.table[0][i].update_value(f"-x{i}")

        for i in range(1, self.e + 1):
            self.table[i][0].update_type(Const.VALUE_CELL)
            self.table[i][0].update_value(vec[i - 1])

        for i in range(1, self.e + 1):
            for j in range(1, self.v + 1):
                self.table[i][j].update_type(Const.COEFFICIENT_CELL)
                self.table[i][j].update_value(mat[i - 1][j - 1])

    def visualize(self):
        rows = self.e + 1
        cols = self.v + 1
        width = 10

        # horizontal separator
        sep = "_" * (cols * (width + 3) - 1)

        for i in range(rows):
            for j in range(cols):
                print(f"{self.table[i][j].get_value()!s:>{width}}", end="")
                if j < cols - 1:
                    print(" | ", end="")
            print()

            if i < rows - 1:
                print(sep)

    def solve():
        pass
