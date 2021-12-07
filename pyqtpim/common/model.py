# 1. system
import datetime
from enum import IntEnum
from typing import Any
import inspect
# 2. PySide
from PySide2 import QtCore
# 3. local
from .settings import MySettings, SetGroup
from .data import Entry, EntryList, EntryListManager


class EntryListModel(QtCore.QAbstractTableModel):
    _data: EntryList
    _fld_names: tuple[tuple[IntEnum, str]]  # FIXME:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
        """TODO: use setHeaderData() in __init__()"""
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._fld_names[section][1]
        return super().headerData(section, orientation, role)

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:  # EditRole for mapper
            c = self._data.item(index.row())
            col = index.column()
            v = c.getPropByName(self._fld_names[col][0])
            if isinstance(v, datetime.datetime):
                v = QtCore.QDateTime(v)
            elif isinstance(v, datetime.date):
                v = QtCore.QDate(v)
            return v

    def columnCount(self, _: QtCore.QModelIndex = None) -> int:
        return len(self._fld_names)

    def rowCount(self, index: QtCore.QModelIndex = None) -> int:
        return self.size

    def insertRows(self, row: int, count: int, parent: QtCore.QModelIndex = None) -> bool:
        self.beginInsertRows(parent, row, row+count-1)
        self._data.insert(row, count)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QtCore.QModelIndex = None) -> bool:
        self.beginRemoveRows(parent, row, row+count-1)
        self._data.remove(row, count)
        self.endRemoveRows()
        return True

    # self
    @property
    def size(self) -> int:
        return self._data.size

    @property
    def path(self) -> str:
        return self._data.path

    def _empty_item(self) -> EntryList:
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")
        return EntryList()

    def switch_data(self, new_el: EntryList = None):
        self.beginResetModel()
        self._data = new_el or self._empty_item()
        self.endResetModel()

    def item(self, i: int) -> Entry:
        return self._data.item(i)


class EntryListManagerModel(QtCore.QStringListModel):  # or QAbstraactListModel
    _set_group: SetGroup
    _data: EntryListManager

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # inherited
    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()].name

    def rowCount(self, index: QtCore.QModelIndex = None) -> int:
        return self.size

    def removeRows(self, row0: int, count: int, _: QtCore.QModelIndex = None) -> bool:
        """Delete 'count' records starting from 'row0'."""
        self.beginRemoveRows(QtCore.QModelIndex(), row0, row0 + count - 1)
        for row in range(row0, row0 + count):
            self._data.itemDel(row)
            MySettings.list_del(self._set_group, row)
        self.endRemoveRows()
        return True

    # self
    def _init_data(self):
        for name, path in MySettings.list_ls(self._set_group):
            self._data.itemAdd(name, path)

    @property
    def size(self) -> int:
        return self._data.size

    def item(self, i: int) -> EntryList:
        return self._data[i]

    def itemAdd(self, name: str, path: str):
        """Add new EntryList
        :todo: implement insertRow() -> bool
        """
        i = self.size
        self.beginInsertRows(QtCore.QModelIndex(), i, i)
        self._data.itemAdd(name, path)
        self.endInsertRows()
        MySettings.list_append(self._set_group, {"name": name, "path": path})

    def itemUpdate(self, idx: QtCore.QModelIndex, name: str, path: str):
        """Update EntryList.
        :todo: implement setData() -> bool
        """
        i = idx.row()
        self._data.itemUpdate(i, name, path)
        MySettings.list_update(self._set_group, i, {"name": name, "path": path})

    def findByName(self, s: str, i: int = None) -> bool:
        """Find existent CL by name [excluding i-th entry]
        :return: True if found
        """
        return self._data.findByName(s, i)

    def findByPath(self, s: str, i: int = None) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        return self._data.findByPath(s, i)
