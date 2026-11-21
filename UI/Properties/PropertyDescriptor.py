from dataclasses import dataclass
from typing import Any

from Unit.Unit import Unit


@dataclass(frozen=True)
class PropertyDescriptor:
    """Описание одного свойства юнита, доступного в инспекторе."""
    name: str
    valueType: type
    readonly: bool

    def read(self, unit: Unit) -> Any:
        return getattr(unit, self.name)

    def write(self, unit: Unit, value: Any) -> None:
        setattr(unit, self.name, value)
