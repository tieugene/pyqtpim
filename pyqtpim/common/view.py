"""vCard/iCal views parents"""

import inspect
from PySide2 import QtCore, QtWidgets
from . import form, data


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
    # _own_model = EntryModel
    _details: EntryView
    actionsChange = QtCore.Signal(bool)

    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent)
        self._details = dependant
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setEditTriggers(self.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        self.setWordWrap(False)
        # __model = self._own_model(self)
        # self.setModel(__model)


class StoreListView(QtWidgets.QListView):
    _model_cls: type
    __form: form.StoreForm
    _list: EntryListView
    _title: str
    actionsChange = QtCore.Signal(bool)

    def __init__(self, parent, dependant: EntryListView):
        super().__init__(parent)
        self._list = dependant
        # self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.MinimumExpanding) - not works
        # self.setMinimumSize(0, 0) - not works
        # self.setSelectionMode(self.SingleSelection)
        self.setEditTriggers(self.NoEditTriggers)
        self.__form = form.StoreForm(self._title)

    def storeAdd(self):
        """Add new Store"""
        if self.__form.exec_new():
            store = self.model().item_cls(self.__form.name, self.__form.connection, self.__form.active)
            self.model().item_add(store)
            self.model().save()

    def storeEdit(self):
        """Edit Store"""
        if not (indexes := self.selectedIndexes()):
            return
        row = indexes[0].row()
        store = self.model().item_get(row)
        if self.__form.exec_edit(store):
            self.model().save()

    def storeDel(self):
        if not (indexes := self.selectedIndexes()):
            return
        row = indexes[0].row()
        store = self.model().item_get(row)
        if QtWidgets.QMessageBox.question(self, f"Deleting {self._title}",
                                          f"Are you sure to delete '{store.name}'")\
                == QtWidgets.QMessageBox.StandardButton.Yes:
            # FIXME: use model method; update model
            self.model().item_del(row)
            self.model().save()

    def storeInfo(self):
        if not (indexes := self.selectedIndexes()):
            return
        store: data.Store = self.model().item_get(indexes[0].row())
        QtWidgets.QMessageBox.information(self, f"{self._title} info",
                                          f"{self._title} info:\n"
                                          f"Name: {store.name}\n"
                                          f"Path: {store.dpath}\n"
                                          f"Active: {store.active}")
