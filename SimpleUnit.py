from CageController import CageController
from Unit import Unit


class SimpleUnit(Unit):
    def run(self, cageController: CageController):
        if self._energy > 0:
            new_simpleUnit = SimpleUnit()
            new_simpleUnit.energy = self._energy // 2
            cageController.worldController.newUnit(1, 0, new_simpleUnit)
            self._energy -= 1

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value

