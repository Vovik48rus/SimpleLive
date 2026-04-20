from __future__ import annotations
from WorldController import WorldController


class CageController:
    def __init__(self, dirt, cage, worldController: WorldController):
        self._dirt = dirt
        self._cage = cage
        self._worldController = worldController

    @property
    def worldController(self) -> WorldController:
        return self._worldController
