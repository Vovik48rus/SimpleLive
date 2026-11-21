from PySide6.QtCore import QObject, Signal

from Unit.Unit import Unit
from World.Handler.ABC.WorldHandlerABC import WorldHandlerABC
from World.WorldGrid import WorldGrid
from World.WorldSimulation import WorldSimulation


class SimulationModel(QObject):
    """Qt-обёртка над WorldSimulation. Единственная точка, через которую
    UI меняет мир; все изменения сообщаются сигналом changed."""
    changed = Signal()
    resized = Signal(int, int)

    def __init__(self, rows: int, cols: int, handler: WorldHandlerABC,
                 parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._simulation = WorldSimulation(WorldGrid(rows, cols))
        self._handler = handler
        self._tick = 0

    @property
    def grid(self) -> WorldGrid:
        # WorldSimulation каждый такт создаёт новую сетку — всегда берём актуальную
        return self._simulation.grid

    @property
    def rows(self) -> int:
        return self.grid.rows

    @property
    def cols(self) -> int:
        return self.grid.cols

    @property
    def tick(self) -> int:
        return self._tick

    def getUnit(self, row: int, col: int) -> Unit:
        return self.grid.getUnit(row, col)

    def setUnit(self, row: int, col: int, unit: Unit) -> None:
        self.grid.setUnit(row, col, unit)
        self.changed.emit()

    def notifyChanged(self) -> None:
        """Вызывать после изменения свойств юнита напрямую."""
        self.changed.emit()

    def setHandler(self, handler: WorldHandlerABC) -> None:
        self._handler = handler

    def step(self) -> None:
        self._simulation.run(self._handler)
        self._tick += 1
        self.changed.emit()

    def clear(self) -> None:
        self._simulation = WorldSimulation(type(self.grid)(self.rows, self.cols))
        self._tick = 0
        self.changed.emit()

    def resize(self, rows: int, cols: int) -> None:
        old = self.grid
        new = type(old)(rows, cols)
        for row in range(min(rows, old.rows)):
            for col in range(min(cols, old.cols)):
                new.setUnit(row, col, old.getUnit(row, col))
        self._simulation = WorldSimulation(new)
        self.resized.emit(rows, cols)
        self.changed.emit()
