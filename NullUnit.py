from CageController import CageController
from NullObject import NullObject
from Unit import Unit


class NullUnit(NullObject, Unit):
    def run(self, cageController: CageController):
        pass
