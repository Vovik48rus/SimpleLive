from abc import ABC

from CageController import CageController


class Unit(ABC):
    def __init__(self):
        self._energy = 10

    @property
    def energy(self) -> int:
        return self._energy

    def run(self, cageController: CageController):
        raise NotImplemented()
