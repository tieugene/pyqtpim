"""vCard/iCal models parents"""

# 1. system
from typing import Any
# 2. PySide
from PySide2 import QtCore
# 3. local
from . import enums
from .data import Store, StoreList, EntryList
from .settings import MySettings


class EntryModel(QtCore.QAbstractTableModel):
    _data: EntryList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Inherit
    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:
        return self._data.size()


class EntryProxyModel(QtCore.QSortFilterProxyModel):
    _own_model = EntryModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSourceModel(self._own_model(self))


class StoreModel(QtCore.QStringListModel):
    _set_group: enums.SetGroup
    item_cls: type
    _data: StoreList
    activeChanged: QtCore.Signal = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Inherit
    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:
        return self._data.size()

    def flags(self, index):
        fl = QtCore.QStringListModel.flags(self, index)
        fl |= QtCore.Qt.ItemIsUserCheckable
        return fl

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return self._data.store_get(index.row()).name
        elif role == QtCore.Qt.CheckStateRole:
            return QtCore.Qt.Checked if self._data.store_get(index.row()).active else QtCore.Qt.Unchecked

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.CheckStateRole:
            row = index.row()
            self._data.store_get(row).active = (value == QtCore.Qt.Checked)
            self.save()
            # TODO: refresh EntryList
            # self.dataChanged.emit(index, index, (role,))
            # self.activeChanged.emit()
            return True
        return False

    # Hand-made
    def item_get(self, i: int) -> Store:
        return self._data.store_get(i)

    def item_add(self, item: Store):
        self.beginInsertRows(self.index(self._data.size(), 0), self._data.size(), self._data.size())
        self._data.store_add(item)
        self.endInsertRows()

    # def item_upd(self, i: int, item: Store):
    #    ...

    def item_del(self, i: int):
        self.beginRemoveRows(self.index(i, 0), i, i)
        self._data.store_del(i)
        self.endRemoveRows()

    def load(self):
        """Load _data from settings"""
        self._data.from_list(MySettings.get(self._set_group, 'store'))

    def save(self):
        """Save _data to settings"""
        MySettings.set(self._set_group, 'store', self._data.to_list())
