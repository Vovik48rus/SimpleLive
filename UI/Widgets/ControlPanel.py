from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QGroupBox, QHBoxLayout, QPushButton,
    QSpinBox, QVBoxLayout, QWidget, QLabel,
)

from UI.Model.EditorState import EditorState
from UI.Model.SimulationModel import SimulationModel
from UI.UiContext import UiContext


class ControlPanel(QWidget):
    """Инструменты редактирования, тип юнита, обработчик и размер мира."""

    def __init__(self, model: SimulationModel, state: EditorState, context: UiContext,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._model = model
        self._context = context

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._buildTools(state, context))
        layout.addWidget(self._buildWorld(model, context))

    def _buildTools(self, state: EditorState, context: UiContext) -> QGroupBox:
        box = QGroupBox("Редактирование")
        layout = QVBoxLayout(box)

        group = QButtonGroup(self)
        group.setExclusive(True)
        row = QHBoxLayout()
        for tool in context.tools:
            button = QPushButton(tool.name)
            button.setCheckable(True)
            button.setChecked(tool is state.tool)
            button.clicked.connect(lambda _=False, t=tool: state.setTool(t))
            group.addButton(button)
            row.addWidget(button)
        layout.addLayout(row)

        combo = QComboBox()
        combo.addItems(context.unitTypes.names())
        combo.currentTextChanged.connect(state.setUnitType)
        state.setUnitType(combo.currentText() or None)
        layout.addWidget(QLabel("Тип юнита для установки"))
        layout.addWidget(combo)
        return box

    def _buildWorld(self, model: SimulationModel, context: UiContext) -> QGroupBox:
        box = QGroupBox("Мир")
        layout = QVBoxLayout(box)

        handlerCombo = QComboBox()
        handlerCombo.addItems(context.handlers.names())
        handlerCombo.currentTextChanged.connect(
            lambda name: model.setHandler(context.handlers.create(name)))
        layout.addWidget(QLabel("Обработчик"))
        layout.addWidget(handlerCombo)

        self._rowsSpin = self._sizeSpin(model.rows)
        self._colsSpin = self._sizeSpin(model.cols)
        sizeRow = QHBoxLayout()
        sizeRow.addWidget(QLabel("Строк"))
        sizeRow.addWidget(self._rowsSpin)
        sizeRow.addWidget(QLabel("Столбцов"))
        sizeRow.addWidget(self._colsSpin)
        layout.addLayout(sizeRow)

        apply = QPushButton("Изменить размер")
        apply.clicked.connect(lambda: model.resize(self._rowsSpin.value(), self._colsSpin.value()))
        layout.addWidget(apply)
        return box

    @staticmethod
    def _sizeSpin(value: int) -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(1, 200)
        spin.setValue(value)
        return spin
