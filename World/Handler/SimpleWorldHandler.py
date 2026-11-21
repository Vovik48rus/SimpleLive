from Unit.NullUnit import NullUnit
from World.Handler.ABC.WorldHandlerABC import WorldHandlerABC


class SimpleWorldHandler(WorldHandlerABC):
    def run(self):
        worldController = self.worldController
        current = worldController.getUnit(0, 0)
        if not issubclass(type(current), NullUnit):
            current.energy -= 1
        if current.energy == 0:
            worldController.setUnit(NullUnit())
        else:
            worldController.setUnit(current)
