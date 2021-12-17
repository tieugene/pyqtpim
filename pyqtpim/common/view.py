"""vCard/iCal views parents"""

import inspect
from PySide2 import QtCore, QtWidgets, QtSql
from .model import EntryModel, StoreModel


class EntryView(QtWidgets.QGroupBox):
    mapper: QtWidgets.QDataWidgetMapper

    def __init__(self, parent):
        super().__init__(parent)
        self.mapper = QtWidgets.QDataWidgetMapper(self)

    def setModel(self, model: QtCore.QStringListModel):
        self.mapper.setModel(model)
        # print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def clean(self):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")


class EntryListView(QtWidgets.QTableView):
    _own_model = EntryModel
    _details: EntryView

    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent)
        self._details = dependant
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        # self.setEditTriggers(self.NoEditTriggers)
        # self.setSortingEnabled(True) # requires sorting itself
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        __model = self._own_model(self)
        self.setModel(__model)

    def entryCat(self):
        print("Stub")

    def entryInside(self):
        print("Stub")


class StoreForm(QtWidgets.QDialog):
    """ A dialog to add (Create) or edit (Update) EL in ELM.
    :todo: chk path exists and is dir"""
    __mapper: QtWidgets.QDataWidgetMapper
    __title: str
    f_name: QtWidgets.QLineEdit
    f_connection: QtWidgets.QLineEdit
    f_active: QtWidgets.QCheckBox

    def __init__(self, title: str, model: QtSql.QSqlTableModel):
        super().__init__()
        self.__title = title
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
        # 4. mapping
        self.__mapper = QtWidgets.QDataWidgetMapper()
        self.__mapper.setModel(model)
        self.__mapper.addMapping(self.f_name, model.fieldIndex('name'))
        self.__mapper.addMapping(self.f_connection, model.fieldIndex('connection'))
        self.__mapper.addMapping(self.f_active, model.fieldIndex('active'))  # FIXME: not writes

    def setIdx(self, idx: QtCore.QModelIndex = None):
        if idx:
            self.__mapper.setCurrentModelIndex(idx)
        else:
            self.f_name.clear()
            self.f_connection.clear()
            self.f_active.setChecked(False)
        act = "Edit" if idx else "Add"
        self.setWindowTitle(f"{act} a {self.__title}")

    def __browse_dir(self):
        # TODO: set starting path
        if directory := QtCore.QDir.toNativeSeparators(
                QtWidgets.QFileDialog.getExistingDirectory(self, "Select dir", QtCore.QDir.currentPath())):
            self.f_connection.setText(directory)

    def __chk_values(self):
        if self.name and self.connection:
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


class StoreListView(QtWidgets.QListView):
    _own_model = StoreModel
    __form: StoreForm
    _list: EntryListView
    _title: str

    def __init__(self, parent, dependant: EntryListView):
        super().__init__(parent)
        self._list = dependant
        # self.setSelectionMode(self.SingleSelection)
        self.setModel(self._own_model())
        self.setModelColumn(self.model().fieldIndex('name'))
        self.setEditTriggers(self.NoEditTriggers)
        self.__form = StoreForm(self._title, self.model())

    def storeAdd(self):
        """Add new Store"""
        self.__form.setIdx()
        if self.__form.exec_():
            rec = self.model().record()
            rec.setValue('name', self.__form.name)
            rec.setValue('connection', self.__form.connection)
            rec.setValue('active', int(self.__form.active))
            ok = self.model().insertRecord(self.model().rowCount(), rec)
            if not ok:
                print("Oops")
            else:
                self.model().updataChildCache()
                self.model().select()   # FIXME: refresh view or model

    def storeEdit(self):
        """Edit Store"""
        if not (indexes := self.selectedIndexes()):
            return
        idx = indexes[0]
        self.__form.setIdx(idx)
        if self.__form.exec_():
            self.model().submit()
            self.model().updataChildCache()

    def storeDel(self):
        if not (indexes := self.selectedIndexes()):
            return
        for index in indexes:
            row = index.row()
            name = self.model().record(row).value('name')
            if QtWidgets.QMessageBox.question(self, f"Deleting {self._title}",
                                              f"Are you sure to delete '{name}'")\
                    == QtWidgets.QMessageBox.StandardButton.Yes:
                self.model().removeRow(row)
                self.model().updataChildCache()
                self.model().select()   # FIXME: refresh view or model

    def storeInfo(self):
        if not (indexes := self.selectedIndexes()):
            return
        rec = self.model().record(indexes[0].row())
        QtWidgets.QMessageBox.information(self, f"{self._title} info",
                                          f"{self._title} info:\n"
                                          f"Name: {rec.value('name')}\n"
                                          f"Path: {rec.value('connection')}")
