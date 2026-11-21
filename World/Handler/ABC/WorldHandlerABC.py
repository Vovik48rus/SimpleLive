from __future__ import annotations
from abc import ABC

from World.WorldController import WorldController


class WorldHandlerABC(ABC):
    _worldController: WorldController

    def __init__(self, worldController: WorldController=None):
        self._worldController = worldController


    @property
    def worldController(self) -> WorldController:
        return self._worldController

    @worldController.setter
    def worldController(self, worldController: WorldController):
        self._worldController = worldController

    def run(self):
        raise NotImplemented
