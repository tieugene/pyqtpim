import inspect
import os.path
from PySide2 import QtCore, QtWidgets, QtSql
from .data import Entry, EntryList
from .model import EntryListModel, EntryListManagerModel


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
    __details: EntryView

    def __init__(self, parent, dependant: EntryView):
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
        # self.resizeColumnsToContents() - QTableView only

    def _empty_model(self) -> EntryListModel:
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")
        return EntryListModel()

    def refresh(self, data: EntryList = None):
        # print("List refresh call")
        self.model().switch_data(data)
        self.__details.clean()

    def itemCat(self):
        """Show file content"""
        idx = self.selectionModel().currentIndex()
        if idx.isValid():
            i = idx.row()
            item: Entry = self.model().item(i)
            path = item.fpath
            if raw := item.load_raw():
                msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, "File content", path)
                msg.setDetailedText(raw)
                # msg.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                msg.exec_()

    def itemInside(self):
        """Show entry content
        :todo: style it
        Simple:
        msg.setText(raw['summary'])
        for ...
          txt += f"{k}: {v}\n"
        msg.setDetailedText(txt)
        """
        idx = self.selectionModel().currentIndex()
        if idx.isValid():
            i = idx.row()
            raw = self.model().item(i).RawContent()
            # icon, title, text
            msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.NoIcon, "Entry content", '')
            # richtext
            txt = "<html><body><table><tbody>"
            for k, v in raw.items():
                if k == 'description':
                    v = f"<pre>{v}</pre>"
                txt += f"<tr><th>{k}:</th><td>{v}</td></tr>"
            txt += "<tbody></table></body><html>"
            msg.setText(txt)
            msg.setTextFormat(QtCore.Qt.RichText)
            # msg.setSizeGripEnabled(True)  # not works
            msg.exec_()


class EntryListManagerView(QtWidgets.QListView):
    __list: EntryListView
    _title: str

    def __init__(self, parent, dependant: EntryListView):
        super().__init__(parent)
        self.__list = dependant
        # self.setSelectionMode(self.SingleSelection)
        self.setModel(self._empty_model())
        self.setModelColumn(self.model().fieldIndex('name'))
        self.setEditTriggers(self.NoEditTriggers)

    def _empty_model(self) -> EntryListManagerModel:
        print("Virtual EntryListManagerView._empty_model()")
        return EntryListManagerModel(self)

    def itemAdd(self):
        """Add new CL.
        todo: chk path exists and is dir"""
        dialog = EntryListForm(self._title)
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
        """:todo: chk path exists and is dir"""
        if not (indexes := self.selectedIndexes()):
            return
        row = indexes[0].row()
        rec = self.model().record(row)
        old_name = rec.value('name')
        old_path = rec.value('connection')
        old_active = rec.value('active')
        dialog = EntryListForm(self._title, old_name, old_path, old_active)
        if dialog.exec_():
            name = dialog.name
            path = dialog.path
            active = dialog.active
            changed = False
            if name != old_name:
                rec.setValue('name', name)
                changed = True
            if path != old_path:
                rec.setValue('path', path)
                changed = True
            if active != old_active:
                rec.setValue('active', active)
                changed = True
            if changed:
                if self.model().updateRowInTable(row, rec):
                    self.model().select()   # FIXME: update view

    def itemDel(self):
        if not (indexes := self.selectedIndexes()):
            return
        row = indexes[0].row()

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


class EntryListForm(QtWidgets.QDialog):
    """ A dialog to add (Create) or edit (Update) EL in ELM."""
    nameText: QtWidgets.QLineEdit
    pathText: QtWidgets.QLineEdit
    activeBool: QtWidgets.QCheckBox

    def __init__(self, title: str, name: str = None, path: str = None, active: bool = False):
        super().__init__()
        name_label = QtWidgets.QLabel("Name")
        path_label = QtWidgets.QLabel("Path")
        path_button = QtWidgets.QPushButton("...")
        active_label = QtWidgets.QLabel("Active")
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.nameText = QtWidgets.QLineEdit()
        self.pathText = QtWidgets.QLineEdit()
        self.activeBool = QtWidgets.QCheckBox()

        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.nameText, 0, 1, 1, 2)
        grid.addWidget(path_label, 1, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid.addWidget(self.pathText, 1, 1)
        grid.addWidget(path_button, 1, 2)
        grid.addWidget(active_label, 2, 0)
        grid.addWidget(self.activeBool, 2, 1, 1, 2)

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
        self.activeBool.setChecked(active)

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

    @property
    def active(self):
        return self.activeBool.isChecked()
