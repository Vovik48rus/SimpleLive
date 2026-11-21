from typing import get_type_hints

from Unit.NullObject import NullObject
from Unit.Unit import Unit
from UI.ABC.PropertyIntrospectorABC import PropertyIntrospectorABC
from UI.Properties.PropertyDescriptor import PropertyDescriptor


class PropertyIntrospector(PropertyIntrospectorABC):
    """Находит публичные @property в иерархии класса юнита.
    Тип берётся из аннотации возвращаемого значения геттера,
    readonly — если у property нет сеттера. Новые юниты и свойства
    появляются в инспекторе без изменений в UI."""

    def describe(self, unit: Unit) -> list[PropertyDescriptor]:
        if isinstance(unit, NullObject):
            return []

        found: dict[str, property] = {}
        for cls in reversed(type(unit).__mro__):  # от базового к производному
            for name, attr in vars(cls).items():
                if isinstance(attr, property) and not name.startswith("_"):
                    found[name] = attr

        return [
            PropertyDescriptor(name, self._resolveType(unit, name, prop), prop.fset is None)
            for name, prop in found.items()
        ]

    @staticmethod
    def _resolveType(unit: Unit, name: str, prop: property) -> type:
        try:
            hint = get_type_hints(prop.fget).get("return")
        except Exception:
            hint = None
        if isinstance(hint, type):
            return hint
        return type(getattr(unit, name))
