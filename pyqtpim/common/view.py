import inspect
import os.path
from PySide2 import QtCore, QtWidgets
from .data import EntryList
from .model import EntryListModel, EntryListManagerModel


class EntryDetailWidget(QtWidgets.QGroupBox):
    mapper: QtWidgets.QDataWidgetMapper

    def __init__(self, parent):
        super().__init__(parent)
        self.mapper = QtWidgets.QDataWidgetMapper(self)

    def setModel(self, model: QtCore.QStringListModel):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def clean(self):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")


class EntryListView(QtWidgets.QTableView):
    __details: EntryDetailWidget

    def __init__(self, parent, dependant: EntryDetailWidget):
        super().__init__(parent)
        self.__details = dependant
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        # self.setEditTriggers(self.NoEditTriggers)
        # self.setSortingEnabled(True) # requires sorting itself
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        __model = self._empty_model()
        self.setModel(__model)
        self.__details.setModel(__model)
        # signals
        # # self.activated.connect(self.rowChanged)
        self.selectionModel().currentRowChanged.connect(self.__details.mapper.setCurrentModelIndex)

    def _empty_model(self) -> EntryListModel:
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")
        return EntryListModel()

    def refresh(self, data: EntryList = None):
        # print("List refresh call")
        self.model().switch_data(data)
        self.__details.clean()


class EntryListManagerView(QtWidgets.QListView):
    __list: EntryListView
    _title: str

    def __init__(self, parent, dependant: EntryListView):
        super().__init__(parent)
        self.__list = dependant
        self.setSelectionMode(self.SingleSelection)
        self.setModel(self._empty_model())
        # set model required
        self.selectionModel().currentRowChanged.connect(self.rowChanged)

    def _empty_model(self) -> EntryListManagerModel:
        print("Virtual EntryListManagerView._empty_model()")
        return EntryListManagerModel()

    def itemAdd(self):
        """Add new CL."""
        dialog = EntryListCUDialog(self._title)
        while dialog.exec_():
            name = dialog.name
            path = dialog.path
            # check values
            # - name is uniq
            if self.model().findByName(name):
                QtWidgets.QMessageBox.warning(self, "Duplicated 'name'",
                                              f"{self._title} with name '{name}' already registered")
                continue
            # - path is uniq
            if self.model().findByPath(path):
                QtWidgets.QMessageBox.warning(self, "Duplicated 'path'",
                                              f"{self._title} with path '{path}' already registered")
                continue
            # - path exists and is dir
            if not os.path.isdir(path):
                QtWidgets.QMessageBox.warning(self, "Wrong 'path'", f"Path '{path}' is not dir or not exists")
                continue
            self.model().itemAdd(name, path)    # update UI
            break

    def itemEdit(self):
        indexes = self.selectionModel().selectedRows()
        if not indexes:
            return
        idx = indexes[0]
        i = idx.row()
        cl = self.model().item(i)
        dialog = EntryListCUDialog(self._title, cl.name, cl.path)
        while dialog.exec_():
            name = dialog.name
            path = dialog.path
            # check values
            # - changed
            if name == cl.name and path == cl.path:  # nothing changed
                break
            # - name is uniq but not this
            if self.model().findByName(name, i):
                QtWidgets.QMessageBox.warning(self, "Traversal 'name'",
                                              f"There is another {self._title} with name '{name}'")
                continue
            # - path is uniq but not this
            if self.model().findByPath(path, i):
                QtWidgets.QMessageBox.warning(self, "Traversal 'path'",
                                              f"There is another {self._title} with path '{path}'")
                continue
            # - path exists and is dir
            if not os.path.isdir(path):
                QtWidgets.QMessageBox.warning(self, "Wrong 'path'",
                                              f"Path '{path}' is not dir or not exists")
                continue
            self.model().itemUpdate(idx, name, path)    # update UI
            break

    def itemDel(self):
        indexes = self.selectionModel().selectedRows()
        for index in indexes:
            i = index.row()
            name = self.model().item(i).name
            if QtWidgets.QMessageBox.question(self, f"Deleting {self._title}",
                                              f"Are you sure to delete '{name}'")\
                    == QtWidgets.QMessageBox.StandardButton.Yes:
                self.model().removeRow(i)

    def itemInfo(self):
        indexes = self.selectionModel().selectedRows()
        if not indexes:
            return
        idx = indexes[0]
        cl = self.model().item(idx.row())
        QtWidgets.QMessageBox.information(self, f"{self._title} info",
                                          f"EntryList info:\n"
                                          f"Name: {cl.name}\n"
                                          f"Path: {cl.path}\n"
                                          f"Records: {cl.size}")

    def rowChanged(self, cur: QtCore.QModelIndex, _: QtCore.QModelIndex):
        """Fully refresh EL widget on ELM row changed"""
        if cur.isValid():
            self.__list.refresh(self.model().item(cur.row()))
        else:
            # print("No list selected")
            self.__list.refresh()


class EntryListCUDialog(QtWidgets.QDialog):
    """ A dialog to add (Create) or edit (Update) EL in ELM."""
    nameText: QtWidgets.QLineEdit
    pathText: QtWidgets.QLineEdit

    def __init__(self, title: str, name: str = None, path: str = None):
        super().__init__()
        name_label = QtWidgets.QLabel("Name")
        path_label = QtWidgets.QLabel("Path")
        path_button = QtWidgets.QPushButton("...")
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.nameText = QtWidgets.QLineEdit()
        self.pathText = QtWidgets.QLineEdit()

        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.nameText, 0, 1, 1, 2)
        grid.addWidget(path_label, 1, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid.addWidget(self.pathText, 1, 1)
        grid.addWidget(path_button, 1, 2)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(button_box)
        self.setLayout(layout)

        path_button.clicked.connect(self.browse_dir)
        button_box.accepted.connect(self.chk_values)
        button_box.rejected.connect(self.reject)
        act = "Edit" if name or path else "Add"
        self.setWindowTitle(f"{act} a {title}")

        if name:
            self.nameText.setText(name)
        if path:
            self.pathText.setText(path)

    def browse_dir(self):
        # TODO: set starting path
        if directory := QtCore.QDir.toNativeSeparators(
                QtWidgets.QFileDialog.getExistingDirectory(self, "Select dir", QtCore.QDir.currentPath())):
            self.pathText.setText(directory)

    def chk_values(self):
        if self.name and self.path:
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Empty values", "As 'name' as 'path' must not be empty")

    @property
    def name(self):
        return self.nameText.text()

    @property
    def path(self):
        return self.pathText.text()
