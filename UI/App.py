import sys

from PySide6.QtWidgets import QApplication

from UI.Bootstrap import createDefaultContext
from UI.Model.EditorState import EditorState
from UI.Model.SimulationModel import SimulationModel
from UI.UiContext import UiContext
from UI.Widgets.MainWindow import MainWindow


def run(context: UiContext | None = None, rows: int = 12, cols: int = 12) -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    context = context or createDefaultContext()

    handler = context.handlers.create(context.handlers.names()[0])
    model = SimulationModel(rows, cols, handler)
    state = EditorState(context.tools[0])

    unitNames = context.unitTypes.names()
    if unitNames:  # как в main.py: один юнит в центре
        model.setUnit(rows // 2, cols // 2, context.unitTypes.create(unitNames[0]))

    window = MainWindow(model, state, context)
    window.show()
    return app.exec()
