from PySide2 import QtWidgets, QtCore
from core.base import data


class StoreForm(QtWidgets.QDialog):
    """ A dialog to create) or update Store.
    :todo: chk path exists and is dir"""
    __title: str
    store: data.Store
    f_name: QtWidgets.QLineEdit
    f_connection: QtWidgets.QLineEdit
    f_active: QtWidgets.QCheckBox

    def __init__(self, title: str):
        super().__init__()
        self.__title = title
        self.store = None
        # 1. widets
        l_name = QtWidgets.QLabel("Name")
        l_connection = QtWidgets.QLabel("Path")
        b_connection = QtWidgets.QPushButton('…')
        l_active = QtWidgets.QLabel("Active")
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.f_name = QtWidgets.QLineEdit()
        self.f_connection = QtWidgets.QLineEdit()
        self.f_active = QtWidgets.QCheckBox()
        # 2. layout
        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        grid.addWidget(l_name, 0, 0)
        grid.addWidget(self.f_name, 0, 1, 1, 2)
        grid.addWidget(l_connection, 1, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid.addWidget(self.f_connection, 1, 1)
        grid.addWidget(b_connection, 1, 2)
        grid.addWidget(l_active, 2, 0)
        grid.addWidget(self.f_active, 2, 1, 1, 2)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(button_box)
        self.setLayout(layout)
        # 3. signal
        b_connection.clicked.connect(self.__browse_dir)
        button_box.accepted.connect(self.__chk_values)
        button_box.rejected.connect(self.reject)

    def __reset(self):
        self.f_name.clear()
        self.f_connection.clear()
        self.f_active.setChecked(False)

    def __set(self, store: data.Store):
        self.f_name.setText(store.name)
        self.f_connection.setText(store.dpath)
        self.f_active.setChecked(store.active)

    def exec_new(self) -> bool:
        self.setWindowTitle(f"New {self.__title}")
        self.__reset()
        if self.exec_():
            return True
        return False

    def exec_edit(self, store: data.Store) -> bool:
        self.setWindowTitle(f"New {self.__title}")
        self.__set(store)
        if self.exec_():
            store.name = self.f_name.text()
            store.dpath = self.f_connection.text()
            store.active = self.f_active.isChecked()
            return True
        return False

    def __browse_dir(self):
        # TODO: set starting path
        if directory := QtCore.QDir.toNativeSeparators(
                QtWidgets.QFileDialog.getExistingDirectory(self, "Select dir", QtCore.QDir.currentPath())):
            self.f_connection.setText(directory)

    def __chk_values(self):
        if self.name and self.connection:
            # TODO: check chg
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Empty values", "As 'name' as 'path' must not be empty")

    @property
    def name(self):
        return self.f_name.text()

    @property
    def connection(self):
        return self.f_connection.text()

    @property
    def active(self):
        return self.f_active.isChecked()
