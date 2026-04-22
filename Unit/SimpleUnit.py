from Unit.Unit import Unit


class SimpleUnit(Unit):

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
