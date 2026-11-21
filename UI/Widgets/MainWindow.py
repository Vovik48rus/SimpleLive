from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDockWidget, QLabel, QMainWindow, QSpinBox, QVBoxLayout, QWidget,
)

from UI.ABC.ToolABC import ToolContext
from UI.Model.EditorState import EditorState
from UI.Model.SimulationModel import SimulationModel
from UI.UiContext import UiContext
from UI.Widgets.ControlPanel import ControlPanel
from UI.Widgets.GridView import GridView
from UI.Widgets.InspectorPanel import InspectorPanel


class MainWindow(QMainWindow):
    def __init__(self, model: SimulationModel, state: EditorState, context: UiContext,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("SimpleLive")
        self.resize(1000, 680)
        self._model = model
        self._state = state

        toolContext = ToolContext(model, state, context.unitTypes)
        self.setCentralWidget(GridView(model, state, context.renderers, toolContext))

        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(model.step)

        self._buildToolbar()
        self._buildSidePanel(model, state, context)

        self._tickLabel = QLabel()
        self.statusBar().addPermanentWidget(self._tickLabel)
        model.changed.connect(self._updateStatus)
        model.resized.connect(self._onResized)
        self._updateStatus()

    def _buildToolbar(self) -> None:
        bar = self.addToolBar("Симуляция")
        bar.setMovable(False)

        self._playAction = QAction("Старт", self)
        self._playAction.setCheckable(True)
        self._playAction.setShortcut("Space")
        self._playAction.toggled.connect(self._onPlayToggled)
        bar.addAction(self._playAction)

        stepAction = QAction("Шаг", self)
        stepAction.setShortcut("N")
        stepAction.triggered.connect(lambda: self._model.step())
        bar.addAction(stepAction)

        clearAction = QAction("Очистить", self)
        clearAction.triggered.connect(lambda: self._model.clear())
        bar.addAction(clearAction)

        bar.addSeparator()
        bar.addWidget(QLabel(" Скорость "))
        speed = QSpinBox()
        speed.setRange(1, 60)
        speed.setValue(5)
        speed.setSuffix(" шаг/с")
        speed.valueChanged.connect(lambda v: self._timer.setInterval(max(1, 1000 // v)))
        bar.addWidget(speed)

    def _buildSidePanel(self, model: SimulationModel, state: EditorState, context: UiContext) -> None:
        side = QWidget()
        layout = QVBoxLayout(side)
        layout.addWidget(ControlPanel(model, state, context))
        layout.addWidget(InspectorPanel(model, state, context.introspector, context.editors))
        layout.addStretch()

        dock = QDockWidget("Панель", self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setWidget(side)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def _onPlayToggled(self, running: bool) -> None:
        self._playAction.setText("Пауза" if running else "Старт")
        if running:
            self._timer.start()
        else:
            self._timer.stop()

    def _onResized(self, rows: int, cols: int) -> None:
        cell = self._state.selectedCell
        if cell is not None and (cell[0] >= rows or cell[1] >= cols):
            self._state.select(None)

    def _updateStatus(self) -> None:
        self._tickLabel.setText(f"Такт: {self._model.tick}   Поле: {self._model.rows}×{self._model.cols}")
