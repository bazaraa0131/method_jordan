import copy
from fractions import Fraction

import const as Const

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

def strip_negation(cell: Cell):
    cell.update_value(cell.get_value().strip('-'))

def invert(frac: Fraction):
    return Fraction(frac.denominator, frac.numerator)

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

    # second line: column names
    cols = list(map(str, src().split()))
    if len(cols) != v:
        raise ValueError(f"Expected {v} values on line 1, got {len(cols)}")

    # each line: v coefficients + 1 RHS
    for r in range(e):
        row = list(map(Fraction, src().split()))
        if len(row) != v + 1:
            raise ValueError(f"Expected {v+1} values on line {r+1}, got {len(row)}")
        mat[r] = row[:v]
        vec[r] = row[v]

    close()
    return e, v, mat, vec, cols

class Solver:
    def __init__(self, from_input = True, input_path = None, method = 2):
        e, v, mat, vec, cols = read(from_input, input_path)

        self.initial_mat = mat
        self.initial_vec = vec

        self.method = method

        self.anchor_row = set()
        self.anchor_col = set()

        self.e = e
        self.v = v

        self.table = [[Cell() for _ in range(self.v + 1)] for _ in range(e + 1)]

        self.table[0][0].update_value("#")

        method_sep = 1 if method == 2 else -1

        for i in range(1, self.v + 1):
            self.table[0][i].update_type(Const.VARIABLE_CELL)
            # self.table[0][i].update_value(f"-x{i}")
            self.table[0][i].update_value(cols[i - 1])

        for i in range(1, self.e + 1):
            self.table[i][0].update_type(Const.VALUE_CELL)
            self.table[i][0].update_value(vec[i - 1])

        for i in range(1, self.e + 1):
            for j in range(1, self.v + 1):
                self.table[i][j].update_type(Const.COEFFICIENT_CELL)
                self.table[i][j].update_value(mat[i - 1][j - 1] * (-1) * method_sep)

    def visualize(self):
        rows = self.e + 1
        cols = self.v + 1

        # horizontal separator
        sep = "_" * (cols * (Const.PRINT_TABLE_FORMAT_WIDTH + 3) - 1)

        for i in range(rows):
            for j in range(cols):
                print(f"{self.table[i][j].get_value()!s:>{Const.PRINT_TABLE_FORMAT_WIDTH}}", end="")
                if j < cols - 1:
                    print(" | ", end="")
            print()

            if i < rows - 1:
                print(sep)

    def choose_anchor_element(self, row, col):

        if len(self.anchor_col) == min(self.e, self.v):
            print("Бүх гол элементийг сонгосон байна.")
            return False
        if row > self.e or col > self.v or row <= 0 or col <= 0:
            print("Дугаарлалт буруу байна.")
            return False
        if row in self.anchor_row:
            print("Аль хэдийн сонгогдсон мөр байна.")
            return False
        if col in self.anchor_col:
            print("Аль хэдийн сонгогдсон багана байна.")
            return False
        if self.table[row][col].get_value() == Fraction(0):
            print("Гол элемент нь 0 байх боломжгүй.")
            return False
        
        self.anchor_row.add(row)
        self.anchor_col.add(col)
        return True

    def perform_step(self):

        row, col = map(int, input("Гол элементээр сонгох элементийн мөр баганын дугаарыг оруулна уу: ").split())

        succes = self.choose_anchor_element(row, col)
        if not succes:
            return False

        t = self.table

        tmp_t = copy.deepcopy(t)
        tmp_t[row][col].update_value(invert(t[row][col].get_value()))

        method_sep = 1 if self.method == 2 else -1

        for i in range(1, self.v + 1):
            if i == col:
                continue
            tmp_t[row][i].update_value(
                method_sep * t[row][i].get_value() / t[row][col].get_value()
            )

        for i in range(1, self.e + 1):
            if i == row:
                continue
            tmp_t[i][col].update_value(
                method_sep * -t[i][col].get_value() / t[row][col].get_value()
            )

        for i in range(1, self.e + 1):
            for j in range(1, self.v + 1):
                if i == row or j == col:
                    continue

                tmp_t[i][j].update_value(
                    (t[i][j].get_value() * t[row][col].get_value()
                    - t[i][col].get_value() * t[row][j].get_value())
                    / t[row][col].get_value()
                )
        
        tmp_t[row][0], tmp_t[0][col] = (tmp_t[0][col], tmp_t[row][0])

        self.table = copy.deepcopy(tmp_t)

        strip_negation(self.table[row][0])
        self.table[0][col].update_value(-self.table[0][col].get_value())

        return True

    def is_finished(self):
        if min(self.e, self.v) == len(self.anchor_col):
            return True
        return False
    
    def is_rank_fin(self):

        for i in range(1, self.e + 1):
            for j in range(1, self.v + 1):
                if i in self.anchor_row or j in self.anchor_col:
                    continue
                if self.table[i][j].get_value() != Fraction(0):
                    return False
        
        return True
    
    def is_solveable(self):
        
        t = self.table

        for i in range(1, self.e + 1):
            if t[i][0].get_type() != Const.VALUE_CELL:
                continue
            accum = Fraction(0)

            for j in range(1, self.v + 1):
                if t[i][j].get_value() != Fraction(0):
                    accum += t[i][j].get_value() * t[0][j].get_value()

            if accum != t[i][0].get_value():
                return False

        return True

    def print_relations(self, print_redundant_relations = False):

        print("\n")

        t = self.table

        for i in range(1, self.e + 1):

            if not print_redundant_relations and t[i][0].get_type() != Const.VARIABLE_CELL:
                continue

            print(f"{t[i][0].get_value()!s:>{Const.PRINT_RELATION_FORMAT_WDITH}}", end=" = ")

            accum = Fraction(0)

            relations = []

            for j in range(1, self.v + 1):
                if t[0][j].get_type() == Const.VALUE_CELL:
                    accum += t[i][j].get_value() * t[0][j].get_value()
                else:
                    relations.append(f"({t[i][j].get_value()!s:>{Const.PRINT_RELATION_FORMAT_WDITH}}) * {t[0][j].get_value()}")
            
            relation_str = " + " + " + ".join(relations) if relations else ""

            print(f"{accum!s:>{Const.PRINT_RELATION_FORMAT_WDITH}}" + relation_str)


        
        
        


