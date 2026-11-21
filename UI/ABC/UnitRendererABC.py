from abc import ABC, abstractmethod

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter

from Unit.Unit import Unit


class UnitRendererABC(ABC):
    """Рисует один юнит в прямоугольнике клетки."""

    @abstractmethod
    def paint(self, painter: QPainter, rect: QRectF, unit: Unit) -> None:
        ...
