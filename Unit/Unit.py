from abc import ABC


class Unit(ABC):
    def __init__(self):
        self._energy = 0

    @property
    def energy(self) -> int:
        return self._energy
