from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from WorldGrid import WorldGrid


class WorldController:
    def __init__(self, world: WorldGrid, newWorldGrid: WorldGrid, row, col):
        self.world: WorldGrid = world
        self.newWorldGrid: WorldGrid = newWorldGrid
        self.col = col
        self.row = row

    def getUnit(self, row, col):
        abs_row = (self.row + row) % self.world.rows
        abs_col = (self.col + col) % self.world.cols
        return self.world.getUnit(abs_row, abs_col)

    def setUnit(self, unit):
        self.newWorldGrid.setUnit(self.row, self.col, unit)
