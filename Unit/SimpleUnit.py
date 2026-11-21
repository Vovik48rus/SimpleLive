from Unit.Unit import Unit


class SimpleUnit(Unit):
    def __init__(self):
        super().__init__()
        self._energy = 10

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
