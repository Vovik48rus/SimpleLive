from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from Unit.Unit import Unit
from World.Handler.ABC.WorldHandlerABC import WorldHandlerABC
from UI.ABC.PropertyIntrospectorABC import PropertyIntrospectorABC
from UI.ABC.ToolABC import ToolABC
from UI.ABC.UnitRendererABC import UnitRendererABC
from UI.Properties.Editors import PropertyEditorABC
from UI.Registry.Registries import NamedRegistry, TypeRegistry


@dataclass
class UiContext:
    """Всё, что можно расширять, собрано в одном месте."""
    unitTypes: NamedRegistry[Callable[[], Unit]]
    handlers: NamedRegistry[Callable[[], WorldHandlerABC]]
    renderers: TypeRegistry[UnitRendererABC]
    editors: TypeRegistry[Callable[[type], PropertyEditorABC]]
    introspector: PropertyIntrospectorABC
    tools: list[ToolABC]
