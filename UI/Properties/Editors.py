from enum import Enum, IntEnum
from typing import Any, Callable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QHBoxLayout,
    QLabel, QLineEdit, QSpinBox, QWidget,
)

from UI.Registry.Registries import TypeRegistry


class PropertyEditorABC(QWidget):
    """Базовый редактор значения. Наследники создают контрол в _createControl,
    сообщают об изменении через valueEdited и принимают значение в setValue."""
    valueEdited = Signal(object)

    def __init__(self, valueType: type, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._valueType = valueType
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._control = self._createControl(valueType)
        layout.addWidget(self._control)

    def _createControl(self, valueType: type) -> QWidget:
        raise NotImplementedError

    def setValue(self, value: Any) -> None:
        raise NotImplementedError

    def isEditing(self) -> bool:
        widget = QApplication.focusWidget()
        return widget is not None and (widget is self or self.isAncestorOf(widget))

    def _silently(self, setter: Callable[[Any], None], value: Any) -> None:
        self._control.blockSignals(True)
        try:
            setter(value)
        finally:
            self._control.blockSignals(False)


class IntEditor(PropertyEditorABC):
    def _createControl(self, valueType: type) -> QWidget:
        box = QSpinBox()
        box.setRange(-10**9, 10**9)
        box.setKeyboardTracking(False)  # значение применяется по Enter / потере фокуса
        box.valueChanged.connect(lambda v: self.valueEdited.emit(v))
        return box

    def setValue(self, value: Any) -> None:
        self._silently(self._control.setValue, int(value))


class FloatEditor(PropertyEditorABC):
    def _createControl(self, valueType: type) -> QWidget:
        box = QDoubleSpinBox()
        box.setRange(-1e9, 1e9)
        box.setDecimals(3)
        box.setSingleStep(0.1)
        box.setKeyboardTracking(False)
        box.valueChanged.connect(lambda v: self.valueEdited.emit(v))
        return box

    def setValue(self, value: Any) -> None:
        self._silently(self._control.setValue, float(value))


class BoolEditor(PropertyEditorABC):
    def _createControl(self, valueType: type) -> QWidget:
        box = QCheckBox()
        box.toggled.connect(lambda v: self.valueEdited.emit(v))
        return box

    def setValue(self, value: Any) -> None:
        self._silently(self._control.setChecked, bool(value))


class StrEditor(PropertyEditorABC):
    def _createControl(self, valueType: type) -> QWidget:
        edit = QLineEdit()
        edit.editingFinished.connect(lambda: self.valueEdited.emit(edit.text()))
        return edit

    def setValue(self, value: Any) -> None:
        self._silently(self._control.setText, str(value))


class EnumEditor(PropertyEditorABC):
    def _createControl(self, valueType: type) -> QWidget:
        self._members = list(valueType)
        box = QComboBox()
        box.addItems([m.name for m in self._members])
        box.currentIndexChanged.connect(lambda i: self.valueEdited.emit(self._members[i]))
        return box

    def setValue(self, value: Any) -> None:
        self._silently(self._control.setCurrentIndex, self._members.index(value))


class LabelEditor(PropertyEditorABC):
    """Запасной вариант для типов без зарегистрированного редактора."""

    def _createControl(self, valueType: type) -> QWidget:
        return QLabel()

    def setValue(self, value: Any) -> None:
        self._control.setText(str(value))


def createDefaultEditorRegistry() -> TypeRegistry[Callable[[type], PropertyEditorABC]]:
    registry: TypeRegistry[Callable[[type], PropertyEditorABC]] = TypeRegistry()
    registry.register(bool, BoolEditor)  # bool раньше int в MRO
    registry.register(int, IntEditor)
    registry.register(float, FloatEditor)
    registry.register(str, StrEditor)
    registry.register(Enum, EnumEditor)
    registry.register(IntEnum, EnumEditor)  # IntEnum раньше int в MRO
    return registry
