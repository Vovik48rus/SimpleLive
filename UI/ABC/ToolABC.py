from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UI.Model.EditorState import EditorState
    from UI.Model.SimulationModel import SimulationModel
    from UI.Registry.Registries import NamedRegistry


@dataclass
class ToolContext:
    model: SimulationModel
    state: EditorState
    unitTypes: NamedRegistry


class ToolABC(ABC):
    """Инструмент мыши: реагирует на нажатие и протягивание по клеткам."""
    name: str = ""

    @abstractmethod
    def press(self, ctx: ToolContext, row: int, col: int) -> None:
        ...

    def drag(self, ctx: ToolContext, row: int, col: int) -> None:
        pass
