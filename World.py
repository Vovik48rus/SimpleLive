from __future__ import annotations
from Cage import Cage
from WorldController import WorldController


class World:
    rows: int
    cols: int
    matrix: list[list[Cage]]

    def __init__(self, rows: int, cols: int) -> None:
        self.matrix = [[Cage() for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols

    def setCage(self, row: int, col: int, cage: Cage):
        self.matrix[row][col] = cage

    def getCage(self, row: int, col: int) -> Cage:
        row = row % self.rows
        col = col % self.cols
        return self.matrix[row][col]

    def run(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.matrix[row][col].run(WorldController(self, row, col))


