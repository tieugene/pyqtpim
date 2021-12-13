from PySide2 import QtWidgets, QtCore

from todo import ColHeader
from common import MySettings, SetGroup


class SettingsView(QtWidgets.QDialog):
    f_todo_col2show: QtWidgets.QListWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__createWidgets()
        self.__setLayout()
        self.setWindowTitle("Settings")
        # TODO: add 'Reset to default' button

    def __createWidgets(self):
        self.f_todo_col2show = QtWidgets.QListWidget()
        self.f_todo_col2show.addItems(ColHeader)
        for i in range(self.f_todo_col2show.count()):
            item = self.f_todo_col2show.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)  # FIXME: |
        # the end
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def __setLayout(self):
        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Columns to show", self.f_todo_col2show)
        # the end
        layout.addRow(self.button_box)
        self.setLayout(layout)

    # Inherit
    def accept(self):
        col2show = set()
        for i in range(self.f_todo_col2show.count()):
            if self.f_todo_col2show.item(i).checkState() == QtCore.Qt.Checked:
                col2show.add(i)
        MySettings.set(SetGroup.ToDo, 'col2show', col2show)
        return super().accept()

    # Hand-made
    def load(self):
        col2show = MySettings.get(SetGroup.ToDo, 'col2show')
        for i in range(self.f_todo_col2show.count()):
            self.f_todo_col2show.item(i).setCheckState(QtCore.Qt.Checked if i in col2show else QtCore.Qt.Unchecked)
