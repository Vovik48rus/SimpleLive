from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter

from Unit.Unit import Unit
from UI.ABC.UnitRendererABC import UnitRendererABC


class EmptyRenderer(UnitRendererABC):
    """Пустая клетка (NullObject): ничего не рисуем."""

    def paint(self, painter: QPainter, rect: QRectF, unit: Unit) -> None:
        pass


class DefaultUnitRenderer(UnitRendererABC):
    """Скруглённый квадрат заданного цвета. Годится для любого юнита."""

    def __init__(self, color: str = "#6c8cff") -> None:
        self._color = QColor(color)

    def paint(self, painter: QPainter, rect: QRectF, unit: Unit) -> None:
        self._drawBody(painter, rect, self._color)

    @staticmethod
    def _drawBody(painter: QPainter, rect: QRectF, color: QColor) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        radius = rect.width() * 0.18
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), radius, radius)

    @staticmethod
    def _drawLabel(painter: QPainter, rect: QRectF, text: str) -> None:
        if rect.height() < 16:
            return
        font = painter.font()
        font.setPixelSize(max(8, int(rect.height() * 0.4)))
        painter.setFont(font)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)


class EnergyUnitRenderer(DefaultUnitRenderer):
    """Прозрачность зависит от energy, число энергии рисуется поверх."""

    def __init__(self, color: str = "#6c8cff", maxEnergy: int = 10) -> None:
        super().__init__(color)
        self._maxEnergy = maxEnergy

    def paint(self, painter: QPainter, rect: QRectF, unit: Unit) -> None:
        ratio = max(0.0, min(1.0, unit.energy / self._maxEnergy))
        fill = QColor(self._color)
        fill.setAlpha(int(70 + 185 * ratio))
        self._drawBody(painter, rect, fill)
        self._drawLabel(painter, rect, str(unit.energy))
