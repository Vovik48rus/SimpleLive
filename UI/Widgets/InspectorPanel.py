from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QVBoxLayout, QWidget

from Unit.Unit import Unit
from UI.ABC.PropertyIntrospectorABC import PropertyIntrospectorABC
from UI.Model.EditorState import EditorState
from UI.Model.SimulationModel import SimulationModel
from UI.Properties.Editors import LabelEditor, PropertyEditorABC
from UI.Properties.PropertyDescriptor import PropertyDescriptor
from UI.Registry.Registries import TypeRegistry


class InspectorPanel(QGroupBox):
    """Показывает и редактирует свойства юнита в выбранной клетке."""

    def __init__(self, model: SimulationModel, state: EditorState,
                 introspector: PropertyIntrospectorABC, editors: TypeRegistry,
                 parent: QWidget | None = None) -> None:
        super().__init__("Юнит", parent)
        self._model = model
        self._state = state
        self._introspector = introspector
        self._editors = editors
        self._unit: Unit | None = None
        self._rows: list[tuple[PropertyDescriptor, PropertyEditorABC]] = []

        self._header = QLabel()
        self._error = QLabel()
        self._error.setStyleSheet("color: #e5484d;")
        self._error.setWordWrap(True)
        self._form = QFormLayout()

        layout = QVBoxLayout(self)
        layout.addWidget(self._header)
        layout.addLayout(self._form)
        layout.addWidget(self._error)

        state.selectionChanged.connect(self._rebuild)
        model.changed.connect(self._onModelChanged)
        self._rebuild()

    def _rebuild(self) -> None:
        while self._form.rowCount():
            self._form.removeRow(0)
        self._rows.clear()
        self._error.clear()
        self._unit = None

        cell = self._state.selectedCell
        if cell is None:
            self._header.setText("Выберите клетку на поле")
            return

        unit = self._model.getUnit(*cell)
        self._unit = unit
        self._header.setText(f"Клетка ({cell[0]}, {cell[1]}): {type(unit).__name__}")

        for descriptor in self._introspector.describe(unit):
            factory = self._editors.find(descriptor.valueType) or LabelEditor
            editor = factory(descriptor.valueType)
            editor.setValue(descriptor.read(unit))
            editor.setEnabled(not descriptor.readonly)
            editor.valueEdited.connect(lambda v, d=descriptor, e=editor: self._onEdited(d, e, v))
            label = descriptor.name + (" (только чтение)" if descriptor.readonly else "")
            self._form.addRow(label, editor)
            self._rows.append((descriptor, editor))

    def _onModelChanged(self) -> None:
        cell = self._state.selectedCell
        if cell is None:
            return
        unit = self._model.getUnit(*cell)
        if unit is not self._unit:
            self._rebuild()  # в клетке теперь другой юнит
            return
        for descriptor, editor in self._rows:
            if not editor.isEditing():
                editor.setValue(descriptor.read(unit))

    def _onEdited(self, descriptor: PropertyDescriptor, editor: PropertyEditorABC, value) -> None:
        try:
            descriptor.write(self._unit, value)
        except Exception as error:  # сеттер юнита может отклонить значение
            self._error.setText(str(error))
            editor.setValue(descriptor.read(self._unit))
            return
        self._error.clear()
        self._model.notifyChanged()
