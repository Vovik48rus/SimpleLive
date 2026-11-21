from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from UI.ABC.ToolABC import ToolContext
from UI.ABC.UnitRendererABC import UnitRendererABC
from UI.Model.EditorState import EditorState
from UI.Model.SimulationModel import SimulationModel
from UI.Registry.Registries import TypeRegistry


class GridView(QWidget):
    """Рисует мир и передаёт мышь активному инструменту."""

    def __init__(self, model: SimulationModel, state: EditorState,
                 renderers: TypeRegistry[UnitRendererABC], context: ToolContext,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._model = model
        self._state = state
        self._renderers = renderers
        self._context = context
        self._lastCell: tuple[int, int] | None = None

        self.setMinimumSize(240, 240)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        model.changed.connect(self.update)
        state.selectionChanged.connect(self.update)

    def _metrics(self) -> tuple[float, float, float]:
        rows, cols = self._model.rows, self._model.cols
        cell = max(1.0, min(self.width() / cols, self.height() / rows))
        return cell, (self.width() - cell * cols) / 2, (self.height() - cell * rows) / 2

    def _cellAt(self, pos: QPointF) -> tuple[int, int] | None:
        cell, ox, oy = self._metrics()
        row = int((pos.y() - oy) // cell)
        col = int((pos.x() - ox) // cell)
        if 0 <= row < self._model.rows and 0 <= col < self._model.cols:
            return row, col
        return None

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rows, cols = self._model.rows, self._model.cols
        cell, ox, oy = self._metrics()

        painter.fillRect(self.rect(), QColor("#14161c"))
        painter.fillRect(QRectF(ox, oy, cell * cols, cell * rows), QColor("#1d2029"))

        if cell >= 6:
            painter.setPen(QPen(QColor("#2b2f3b"), 1))
            for r in range(rows + 1):
                painter.drawLine(QPointF(ox, oy + r * cell), QPointF(ox + cols * cell, oy + r * cell))
            for c in range(cols + 1):
                painter.drawLine(QPointF(ox + c * cell, oy), QPointF(ox + c * cell, oy + rows * cell))

        for r in range(rows):
            for c in range(cols):
                unit = self._model.getUnit(r, c)
                renderer = self._renderers.find(type(unit))
                if renderer is not None:
                    painter.save()
                    renderer.paint(painter, QRectF(ox + c * cell, oy + r * cell, cell, cell), unit)
                    painter.restore()

        selected = self._state.selectedCell
        if selected is not None:
            r, c = selected
            painter.setPen(QPen(QColor("#ffd166"), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(QRectF(ox + c * cell, oy + r * cell, cell, cell).adjusted(1, 1, -1, -1))

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        cell = self._cellAt(event.position())
        self._lastCell = cell
        if cell is not None:
            self._state.tool.press(self._context, *cell)

    def mouseMoveEvent(self, event) -> None:
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        cell = self._cellAt(event.position())
        if cell is not None and cell != self._lastCell:
            self._lastCell = cell
            self._state.tool.drag(self._context, *cell)

    def mouseReleaseEvent(self, event) -> None:
        self._lastCell = None
