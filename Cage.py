from __future__ import annotations

from CageController import CageController
from Dirt import Dirt
from NullObject import NullObject
from NullUnit import NullUnit
from Unit import Unit
from WorldController import WorldController


class Cage:

    def __init__(self, base: Dirt=None, unit: Unit=NullUnit()):
        self._dirt = base
        self._unit = unit

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value: Unit):
        if not issubclass(type(value), NullObject):
            self._unit = value
        else:
            raise NotImplemented()

    @property
    def dirt(self):
        return self._dirt


    def run(self, worldController: WorldController):
        self.unit.run(CageController(self.unit, self.dirt, worldController))
