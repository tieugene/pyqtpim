"""vCard/iCal models parents"""

# 1. system
from typing import Any, Callable
# 2. PySide
from PySide2 import QtCore
# 3. local
from . import enums
from .data import Store, StoreList, Entry, EntryList
from .settings import MySettings


class EntryModel(QtCore.QAbstractTableModel):
    _data: EntryList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Inherit
    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:
        return self._data.size()

    # Hand-made
    def item_add(self, item: Entry) -> bool:  # C
        """Add newly crated Entry.
        :todo: resort/refilter/insert line"""
        return self._data.entry_add(item, new=True)

    def item_get(self, i: int) -> Entry:  # R
        return self._data.entry_get(i)

    def item_upd(self, i: int) -> bool:  # U
        """Flush entry to source file.
        :todo: resort/refilter/update line"""
        return self._data.entry_get(i).save()

    def item_del(self, i: int) -> bool:  # D
        """Remove entry from disk and list
        :todo: line removing handle"""
        return self._data.entry_del(i)


class EntryProxyModel(QtCore.QSortFilterProxyModel):
    # _own_model = EntryModel
    _currentSorter: Callable
    _currentFilter: Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setSourceModel(self._own_model(self))
        self._currentSorter = self._lessThen_None
        self._currentFilter = self._accept_Default

    def refilter(self):
        self.invalidateFilter()

    def resortfilter(self):
        self.invalidate()

    @staticmethod
    def _lessThen_None(source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """Default sorter (no sort)"""
        return source_left.row() < source_right.row()

    @staticmethod
    def _accept_All(_: int) -> bool:
        """Dummy filter (enable all)"""
        return True

    def _accept_Default(self, source_row: int) -> bool:
        """Default filter (enable all)"""
        return self.sourceModel().item_get(source_row).store.active
        # return True


class StoreModel(QtCore.QStringListModel):
    _set_group: enums.SetGroup
    item_cls: type
    _data: StoreList
    _entry_model: EntryModel
    activeChanged: QtCore.Signal = QtCore.Signal()

    def __init__(self, entries: EntryModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entry_model = entries

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
            self.activeChanged.emit()
            return True
        return False

    # Hand-made
    def item_add(self, item: Store):
        self.beginInsertRows(self.index(self._data.size(), 0), self._data.size(), self._data.size())
        self._data.store_add(item)
        self.endInsertRows()

    def item_get(self, i: int) -> Store:
        return self._data.store_get(i)

    # def item_upd(self, i: int, item: Store):
    #    ...

    def item_del(self, i: int):
        self.beginRemoveRows(self.index(i, 0), i, i)
        self._data.store_del(i)
        self.endRemoveRows()

    def item_find(self, item: Store) -> int:
        return self._data.store_find(item)

    def load_self(self):
        """Load _data from settings"""
        self.beginResetModel()
        self._data.from_list(MySettings.get(self._set_group, 'store'))
        self.endResetModel()

    def load_entries(self):
        """Load _data from settings"""
        self._entry_model.beginResetModel()
        self._data.load_entries()
        self._entry_model.endResetModel()

    def save(self):
        """Save _data to settings"""
        MySettings.set(self._set_group, 'store', self._data.to_list())
