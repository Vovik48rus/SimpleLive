from Cage import Cage
from Dirt import Dirt
from NullObject import NullObject
from NullUnit import NullUnit
from SimpleUnit import SimpleUnit
from World import World


def pprint(world):
    for col in range(5):
        for row in range(5):
            if not issubclass(type(world.matrix[row][col].unit), NullUnit):
                print(world.matrix[row][col].unit.energy, end=' ')
            else:
                print(0, end=' ')
        print()


if __name__ == "__main__":
    world = World(5, 5)
    world.setCage(2, 2, Cage(Dirt(), SimpleUnit()))

    pprint(world)
    print()

    while True:
        world.run()

        pprint(world)
        print()
        input()
