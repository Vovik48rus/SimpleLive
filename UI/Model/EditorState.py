from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

if TYPE_CHECKING:
    from UI.ABC.ToolABC import ToolABC


class EditorState(QObject):
    """Состояние редактора: выбранная клетка, инструмент, тип юнита для установки."""
    selectionChanged = Signal()
    toolChanged = Signal()
    unitTypeChanged = Signal()

    def __init__(self, tool: ToolABC, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._tool = tool
        self._selected: tuple[int, int] | None = None
        self._unitTypeName: str | None = None

    @property
    def tool(self) -> ToolABC:
        return self._tool

    def setTool(self, tool: ToolABC) -> None:
        self._tool = tool
        self.toolChanged.emit()

    @property
    def selectedCell(self) -> tuple[int, int] | None:
        return self._selected

    def select(self, cell: tuple[int, int] | None) -> None:
        if cell != self._selected:
            self._selected = cell
            self.selectionChanged.emit()

    @property
    def unitTypeName(self) -> str | None:
        return self._unitTypeName

    def setUnitType(self, name: str | None) -> None:
        self._unitTypeName = name
        self.unitTypeChanged.emit()
