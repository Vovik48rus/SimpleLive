# WorldGrid.py
from __future__ import annotations

from Unit.NullUnit import NullUnit
from Unit.Unit import Unit


class WorldGrid:
    _rows: int
    _cols: int
    matrix: list[list[Unit]]

    def __init__(self, rows: int, cols: int) -> None:
        self.matrix = [[NullUnit() for _ in range(cols)] for _ in range(rows)]
        self._rows = rows
        self._cols = cols

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def setUnit(self, row: int, col: int, unit: Unit):
        self.matrix[row][col] = unit

    def getUnit(self, row: int, col: int) -> Unit:
        row = row % self.rows
        col = col % self.cols
        return self.matrix[row][col]