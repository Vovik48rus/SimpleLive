from Unit.NullObject import NullObject
from Unit.SimpleUnit import SimpleUnit
from Unit.Unit import Unit
from World.Handler.SimpleWorldHandler import SimpleWorldHandler
from UI.Properties.Editors import createDefaultEditorRegistry
from UI.Properties.PropertyIntrospector import PropertyIntrospector
from UI.Registry.Registries import NamedRegistry, TypeRegistry
from UI.Rendering.Renderers import DefaultUnitRenderer, EmptyRenderer, EnergyUnitRenderer
from UI.Tools.Tools import EraseTool, PlaceTool, SelectTool
from UI.UiContext import UiContext


def createDefaultContext() -> UiContext:
    """Композиционный корень UI. Чтобы добавить новый юнит или обработчик,
    зарегистрируйте его здесь (или в своём контексте)."""
    unitTypes = NamedRegistry()
    unitTypes.register("SimpleUnit", SimpleUnit)

    handlers = NamedRegistry()
    handlers.register("SimpleWorldHandler", SimpleWorldHandler)

    renderers = TypeRegistry()
    renderers.register(Unit, DefaultUnitRenderer())
    renderers.register(NullObject, EmptyRenderer())
    renderers.register(SimpleUnit, EnergyUnitRenderer("#6c8cff", maxEnergy=10))

    return UiContext(
        unitTypes=unitTypes,
        handlers=handlers,
        renderers=renderers,
        editors=createDefaultEditorRegistry(),
        introspector=PropertyIntrospector(),
        tools=[SelectTool(), PlaceTool(), EraseTool()],
    )
