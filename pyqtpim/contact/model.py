"""PySide interface"""

# 2. PySide
import typing

from PySide2 import QtCore
# 3. local
from .collection import ContactList, ContactListManager
from settings import MySettings

# const
FIELD_NAMES = (
    ("FN", 'fn'),
    ("Last name", 'family'),
    ("First name", 'given'),
    ("Email", 'email'),
    ("Tel.", 'tel')
)


class ContactListModel(QtCore.QAbstractTableModel):
    __data: ContactList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__data = ContactList()

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> typing.Any:
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.DisplayRole:
            return FIELD_NAMES[section][0]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            c = self.__data.item(index.row())
            col = index.column()
            return c.getPropByName(FIELD_NAMES[col][1])

    def rowCount(self, index):
        return self.size

    def columnCount(self, index):
        return 5

    # self
    @property
    def size(self):
        return self.__data.size

    def switch_data(self, new_cl: ContactList = None):
        self.beginResetModel()
        self.__data = new_cl or ContactList()
        self.endResetModel()

    def item(self, i: int):
        return self.__data.item(i)


class ContactListManagerModel(QtCore.QStringListModel):
    __data: ContactListManager

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__data = ContactListManager()
        self.__init_data()

    # inherited
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()].name

    def rowCount(self, index):
        return self.size

    def removeRows(self, row0: int, count: int, _: QtCore.QModelIndex):
        """Delete count records starting from i."""
        self.beginRemoveRows(QtCore.QModelIndex(), row0, row0 + count - 1)
        for row in range(row0, row0 + count):
            self.__data.itemDel(row)
            MySettings.ab_del(row)
        self.endRemoveRows()
        return True

    # self
    def __init_data(self):
        for name, path in MySettings.AB:
            self.__data.itemAdd(name, path)

    @property
    def size(self):
        return self.__data.size

    def item(self, i: int) -> ContactList:
        return self.__data[i]

    def itemAdd(self, name: str, path: str):
        """Add new ContactList
        :todo: implement insertRow() -> bool
        """
        i = self.size
        self.beginInsertRows(QtCore.QModelIndex(), i, i)
        self.__data.itemAdd(name, path)
        self.endInsertRows()
        MySettings.ab_append({"name": name, "path": path})

    def itemUpdate(self, idx: QtCore.QModelIndex, name: str, path: str):
        """Add new ContactList.
        :todo: implement setData() -> bool
        """
        i = idx.row()
        self.__data.itemUpdate(i, name, path)
        MySettings.ab_update(i, {"name": name, "path": path})

    def findByName(self, s: str, i: int = None) -> bool:
        """Find existent CL by name [excluding i-th entry]
        :return: True if found
        """
        return self.__data.findByName(s, i)

    def findByPath(self, s: str, i: int = None) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        return self.__data.findByPath(s, i)
