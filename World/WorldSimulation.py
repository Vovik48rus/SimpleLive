# WorldSimulation.py
from __future__ import annotations

from World.WorldGrid import WorldGrid
from World.WorldController import WorldController
from World.Handler.ABC.WorldHandlerABC import WorldHandlerABC


class WorldSimulation:
    def __init__(self, grid: WorldGrid) -> None:
        self._grid = grid

    @property
    def grid(self) -> WorldGrid:
        return self._grid

    def run(self, handler: WorldHandlerABC):
        new_worldGrid = type(self._grid)(self.grid.rows, self.grid.cols)

        for row in range(self._grid.rows):
            for col in range(self._grid.cols):
                handler.worldController = WorldController(self._grid, new_worldGrid, row, col)
                handler.run()

        self._grid = new_worldGrid
