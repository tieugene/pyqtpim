"""vCard/iCal models parents"""

# 1. system
# 2. PySide
from typing import Any

from PySide2 import QtCore, QtSql
# 3. local
from .settings import SetGroup


class EntryModel(QtSql.QSqlTableModel):
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
        self.setSort(self.fieldIndex('id'), QtCore.Qt.SortOrder.AscendingOrder)
        self.setHeaderData(self.fieldIndex('id'), QtCore.Qt.Horizontal, 'ID')
        self.setHeaderData(self.fieldIndex('active'), QtCore.Qt.Horizontal, '✓')
        self.setHeaderData(self.fieldIndex('name'), QtCore.Qt.Horizontal, "Name")
        self.setHeaderData(self.fieldIndex('connection'), QtCore.Qt.Horizontal, "Connection")
        self.select()

    # Inherit
    def flags(self, index):
        fl = QtSql.QSqlTableModel.flags(self, index)
        if index.column() == self.fieldIndex('name'):
            fl |= QtCore.Qt.ItemIsUserCheckable
        return fl

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole) -> Any:
        if role == QtCore.Qt.CheckStateRole \
                and ((self.flags(index) & QtCore.Qt.ItemIsUserCheckable) != QtCore.Qt.NoItemFlags):
            return QtCore.Qt.Checked if bool(self.data(index.siblingAtColumn(self.fieldIndex('active')))) \
                    else QtCore.Qt.Unchecked
        else:
            return QtSql.QSqlTableModel.data(self, index, role)

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.CheckStateRole and \
                (self.flags(index) & QtCore.Qt.ItemIsUserCheckable != QtCore.Qt.NoItemFlags):
            self.setData(index.siblingAtColumn(self.fieldIndex('active')), 1 if value == QtCore.Qt.Checked else 0)
            self.submit()
            # self.dataChanged.emit(index, index, (role,))
            self.activeChanged.emit()
            return True
        return QtSql.QSqlTableModel.setData(self, index, value, role)
