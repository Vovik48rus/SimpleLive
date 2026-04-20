from __future__ import annotations

from NullObject import NullObject

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from World import World


class WorldController:
    def __init__(self, world, row, col):
        self.world: World = world
        self.col = col
        self.row = row

    def getCage(self):
        pass

    def newUnit(self, row, col, unit):
        col = self.col + col
        if col >= self.world.rows:
            return
        row = (self.row + row) % self.world.cols
        real_cage = self.world.getCage(row, col)
        if issubclass(type(real_cage.unit), NullObject):
            real_cage.unit = unit
