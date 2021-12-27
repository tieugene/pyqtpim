"""vCard/iCal views parents"""

import inspect
from PySide2 import QtCore, QtWidgets
from .model import EntryModel
from . import enums, form
from .data import Store


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
        self.setWordWrap(False)
        __model = self._own_model(self)
        self.setModel(__model)

    def entryCat(self):
        print("Stub")

    def entryInside(self):
        print("Stub")


class StoreListView(QtWidgets.QListView):
    _model_cls: type
    __form: form.StoreForm
    _list: EntryListView
    _title: str

    def __init__(self, parent, dependant: EntryListView):
        super().__init__(parent)
        self._list = dependant
        # self.setSelectionMode(self.SingleSelection)
        self.setModel(self._model_cls())
        self.setModelColumn(enums.EColNo.Name.value)
        self.setEditTriggers(self.NoEditTriggers)
        self.__form = form.StoreForm(self._title)

    def storeAdd(self):
        """Add new Store"""
        if self.__form.exec_new():
            # FIXME: use model method; update model
            # s_list: StoreList = self.model()._data
            # store = s_list._item_cls(self.__form.name, self.__form.connection, self.__form.active)
            # s_list.store_add(store)
            store = self.model().item_cls(self.__form.name, self.__form.connection, self.__form.active)
            self.model().item_add(store)
            self.model().save()

    def storeEdit(self):
        """Edit Store"""
        if not (indexes := self.selectedIndexes()):
            return
        row = indexes[0].row()
        # s_list: StoreList = self.model()._data
        # store: Store = s_list.store(row)
        store = self.model().item_get(row)
        if self.__form.exec_edit(store):
            # FIXME: use model method; update model row
            self.model().save()

    def storeDel(self):
        if not (indexes := self.selectedIndexes()):
            return
        row = indexes[0].row()
        # s_list: StoreList = self.model()._data
        # store: Store = s_list.store(row)
        store = self.model().item_get(row)
        if QtWidgets.QMessageBox.question(self, f"Deleting {self._title}",
                                          f"Are you sure to delete '{store.name}'")\
                == QtWidgets.QMessageBox.StandardButton.Yes:
            # FIXME: use model method; update model
            # s_list.store_del(row)
            self.model().item_del(row)
            self.model().save()

    def storeInfo(self):
        if not (indexes := self.selectedIndexes()):
            return
        store: Store = self.model().item_get(indexes[0].row())
        QtWidgets.QMessageBox.information(self, f"{self._title} info",
                                          f"{self._title} info:\n"
                                          f"Name: {store.name}\n"
                                          f"Path: {store.dpath}\n"
                                          f"Active: {store.active}")
