from Unit.NullUnit import NullUnit
from UI.ABC.ToolABC import ToolABC, ToolContext


class SelectTool(ToolABC):
    name = "Выбрать"

    def press(self, ctx: ToolContext, row: int, col: int) -> None:
        ctx.state.select((row, col))


class PlaceTool(ToolABC):
    name = "Поставить"

    def press(self, ctx: ToolContext, row: int, col: int) -> None:
        self._place(ctx, row, col)
        ctx.state.select((row, col))

    def drag(self, ctx: ToolContext, row: int, col: int) -> None:
        self._place(ctx, row, col)

    @staticmethod
    def _place(ctx: ToolContext, row: int, col: int) -> None:
        typeName = ctx.state.unitTypeName
        if typeName is not None:
            ctx.model.setUnit(row, col, ctx.unitTypes.create(typeName))


class EraseTool(ToolABC):
    name = "Стереть"

    def press(self, ctx: ToolContext, row: int, col: int) -> None:
        ctx.model.setUnit(row, col, NullUnit())

    def drag(self, ctx: ToolContext, row: int, col: int) -> None:
        self.press(ctx, row, col)
