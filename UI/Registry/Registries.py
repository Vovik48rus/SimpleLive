from typing import Callable


class TypeRegistry[T]:
    """Значение по типу с учётом наследования: подкласс использует
    рендерер/редактор родителя, пока для него не зарегистрирован свой."""

    def __init__(self) -> None:
        self._items: dict[type, T] = {}

    def register(self, type_: type, item: T) -> None:
        self._items[type_] = item

    def find(self, type_: type) -> T | None:
        for cls in type_.__mro__:
            if cls in self._items:
                return self._items[cls]
        return None


class NamedRegistry[T]:
    """Именованные фабрики (типы юнитов, обработчики) в порядке регистрации."""

    def __init__(self) -> None:
        self._factories: dict[str, Callable[[], T]] = {}

    def register(self, name: str, factory: Callable[[], T]) -> None:
        self._factories[name] = factory

    def names(self) -> list[str]:
        return list(self._factories)

    def create(self, name: str) -> T:
        return self._factories[name]()
