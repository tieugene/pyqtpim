# 1. system
# 2. PySide
from PySide2 import QtCore
# 3. local
from common.settings import MySettings
from common.backend import EntryList, EntryListManager


class EntryListModel(QtCore.QAbstractTableModel):
    _data: EntryList
    _fld_names: tuple

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int):
        """TODO: use setHeaderData() in __init__()"""
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._fld_names[section][0]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:  # EditRole for mapper
            c = self._data.item(index.row())
            col = index.column()
            return c.getPropByName(self._fld_names[col][1])

    def rowCount(self, index):
        return self.size

    # self
    @property
    def size(self):
        return self._data.size

    def _empty_item(self) -> EntryList:
        print("Virtual EntryListModel._switch_itself")
        return EntryList()

    def switch_data(self, new_el: EntryList = None):
        self.beginResetModel()
        self._data = new_el or self._empty_item()
        self.endResetModel()

    def item(self, i: int):
        return self._data.item(i)


class EntryListManagerModel(QtCore.QStringListModel):  # or QAbstraactListModel
    _set_group: str
    _data: EntryListManager

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # inherited
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()].name

    def rowCount(self, index):
        return self.size

    def removeRows(self, row0: int, count: int, _: QtCore.QModelIndex):
        """Delete count records starting from i."""
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
    def size(self):
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
