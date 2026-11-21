from abc import ABC, abstractmethod

from Unit.Unit import Unit
from UI.Properties.PropertyDescriptor import PropertyDescriptor


class PropertyIntrospectorABC(ABC):
    """Определяет, какие свойства юнита показывать и редактировать."""

    @abstractmethod
    def describe(self, unit: Unit) -> list[PropertyDescriptor]:
        ...
