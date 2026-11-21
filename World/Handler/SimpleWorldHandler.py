from Unit.NullUnit import NullUnit
from Unit.SimpleUnit import SimpleUnit
from World.Handler.ABC.WorldHandlerABC import WorldHandlerABC


class SimpleWorldHandler(WorldHandlerABC):
    def run(self):
        worldController = self.worldController

        summ = 0
        current = worldController.getUnit(0, 0)
        for i in range(-1, 2):
            for j in range(-1, 2):
                summ += worldController.getUnit(i, j).energy
        add_energy = 1 if summ < 10 else (0 if summ < 20 else -1)
        if not issubclass(type(current), NullUnit):
            current.energy += add_energy


        if add_energy > 0 and issubclass(type(current), NullUnit):
            s_u = SimpleUnit()
            s_u.energy = add_energy
            worldController.setUnit(s_u)
        elif current.energy <= 0:
            worldController.setUnit(NullUnit())
        else:
            worldController.setUnit(current)
