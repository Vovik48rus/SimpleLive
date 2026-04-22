from Unit.NullUnit import NullUnit
from Unit.SimpleUnit import SimpleUnit
from SimpleWorldHandler import SimpleWorldHandler
from WorldGrid import WorldGrid
from WorldSimulation import WorldSimulation


def pprint(world):
    for col in range(5):
        for row in range(5):
            if not issubclass(type(world.matrix[row][col]), NullUnit):
                print(world.matrix[row][col].energy, end=' ')
            else:
                print(0, end=' ')
        print()


if __name__ == "__main__":
    world = WorldGrid(5, 5)
    world.setUnit(2, 2, SimpleUnit())

    pprint(world)
    print()
    simpleWorldHandler = SimpleWorldHandler()

    sim = WorldSimulation(world)

    while True:
        sim.run(simpleWorldHandler)

        pprint(world)
        print()
        input()
