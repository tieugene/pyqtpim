"""vCard/iCal models parents"""

# 1. system
from typing import Any
# 2. PySide
from PySide2 import QtCore, QtSql
# 3. local
from .settings import SetGroup
from . import enums


class EntryModel(QtSql.QSqlQueryModel):
    store_name = dict()  # class-wide cache of Store names (id:name)
    _own_query: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EntryProxyModel(QtCore.QSortFilterProxyModel):
    _own_model = EntryModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSourceModel(self._own_model(self))


class StoreModel(QtSql.QSqlTableModel):
    activeChanged: QtCore.Signal = QtCore.Signal()
    _set_group: SetGroup

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable("store")
        self.setSort(enums.EColNo.ID.value, QtCore.Qt.SortOrder.AscendingOrder)
        self.select()
        self.updataChildCache()

    # Inherit
    def flags(self, index):
        fl = QtSql.QSqlTableModel.flags(self, index)
        if index.column() == enums.EColNo.Name:
            fl |= QtCore.Qt.ItemIsUserCheckable
        return fl

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if role == QtCore.Qt.CheckStateRole \
                and ((self.flags(index) & QtCore.Qt.ItemIsUserCheckable) != QtCore.Qt.NoItemFlags):
            return QtCore.Qt.Checked if bool(self.data(index.siblingAtColumn(enums.EColNo.Active.value))) \
                    else QtCore.Qt.Unchecked
        else:
            return QtSql.QSqlTableModel.data(self, index, role)

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.CheckStateRole and \
                (self.flags(index) & QtCore.Qt.ItemIsUserCheckable != QtCore.Qt.NoItemFlags):
            self.setData(index.siblingAtColumn(enums.EColNo.Active.value), 1 if value == QtCore.Qt.Checked else 0)
            self.submit()
            # self.dataChanged.emit(index, index, (role,))
            self.activeChanged.emit()
            return True
        return QtSql.QSqlTableModel.setData(self, index, value, role)

    # Hand-made
    def updataChildCache(self):
        """Update child model's cache"""
        EntryModel.store_name.clear()
        for i in range(self.rowCount()):
            EntryModel.store_name[self.record(i).value(enums.EColNo.ID.value)] =\
                self.record(i).value(enums.EColNo.Name.value)
