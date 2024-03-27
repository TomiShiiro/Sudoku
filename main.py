import random
import numpy as np

EMPTY_VALUE = 0


class SudokuSolver:

    def __init__(
        self, field: np.ndarray | None = None, n_rows: int = 9, n_columns: int = 9
    ):

        if field is None:
            field = np.zeros([n_rows, n_columns], dtype=int)
        self.field = field
        self.n_rows = n_rows
        self.n_columns = n_columns

    def check_sequence(self, sequence: np.ndarray):  # 1.
        nonZeroesSeq = sequence[sequence != 0]
        return len(np.unique(nonZeroesSeq)) == len(nonZeroesSeq)

    def check_one_cell(self, row_index: int, column_index: int):  # 3.
        return (
            self.check_row(row_index)
            and self.check_column(column_index)
            and self.check_block(row_index, column_index)
        )

    def check_row(self, row_index: int):  # 2.
        return self.check_sequence(self.field[row_index, :])

    def check_column(self, column_index: int):  # 3.
        return self.check_sequence(self.field[:, column_index])

    def check_block(self, row_index: int, column_index: int):  # 3.
        block_row = row_index // 3
        block_col = column_index // 3
        block_slice = self.field[
            block_row * 3 : block_row * 3 + 3, block_col * 3 : block_col * 3 + 3
        ]
        return self.check_sequence(block_slice)

    def is_complete(self):
        return len(self.field[self.field == 0]) == 0

    def solve(self):  # 5.
        if self.is_complete():
            return True

        for i in range(9):
            for j in range(9):
                if self.field[i, j] == 0:
                    for num in range(1, 10):
                        self.field[i, j] = num
                        if self.check_field():
                            if self.solve():
                                return True
                        self.field[i, j] = 0
                    return False

    def check_field(self):  # 4.
        for i in range(9):
            for j in range(9):
                if not self.check_one_cell(i, j):
                    return False
        return True

    def load(self, path):
        with open(path) as f:
            lines = f.readlines()
            numeric_lines = [
                [int(v) for v in line.strip().split(";")] for line in lines
            ]
            self.field = np.array(numeric_lines)


def main():
    sudoku_solver = SudokuSolver()
    sudoku_solver.load("data/game.csv")

    print(sudoku_solver.solve())
    print(sudoku_solver.field)


if __name__ == "__main__":
    main()
