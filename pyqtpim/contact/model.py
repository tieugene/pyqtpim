"""PySide interface"""

# 2. PySide
import typing

from PySide2 import QtCore
# 3. local
from .collection import ABs, ContactList, ContactListManager

# const
FIELD_NAMES = (
    ("FN", 'fn'),
    ("Last name", 'family'),
    ("First name", 'given'),
    ("Email", 'email'),
    ("Tel.", 'tel')
)


class ContactListModel(QtCore.QAbstractTableModel):
    cl: ContactList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cl = ContactList()

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> typing.Any:
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.DisplayRole:
            return FIELD_NAMES[section][0]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            c = self.cl[index.row()]
            col = index.column()
            return c.getByName(FIELD_NAMES[col][1])

    def rowCount(self, index):
        return self.size

    def columnCount(self, index):
        return 5

    # self
    @property
    def size(self):
        return self.cl.size

    def getBack(self, index):
        """Get inner data"""
        return self.cl[index.row()]


class ContactListManagerModel(QtCore.QAbstractListModel):
    clm: ContactListManager

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clm = ContactListManager()
        self.__init_data()

    # inherited
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            name, _ = self.clm[index.row()]
            return name

    def rowCount(self, index):
        return self.size

    # self
    @property
    def size(self):
        return self.clm.size

    def __init_data(self):
        """:todo: lazy load"""
        for name, path in ABs:
            self.clm.itemAdd(name, path)

    def itemAdd(self, name: str, path: str):
        """Add new ContactList
        :todo: implenet insertRow() -> bool
        """
        i = self.size
        self.beginInsertRows(QtCore.QModelIndex(), i, i)
        self.clm.itemAdd(name, path)
        self.endInsertRows()
        # update settings (TODO: to handmade QSettings successor)
        s = QtCore.QSettings()
        s.beginGroup("contacts")
        s.beginWriteArray("sources")
        s.setArrayIndex(i)
        s.setValue("name", name)
        s.setValue("path", path)
        s.endArray()
        s.endGroup()

    def itemUpdate(self, idx: QtCore.QModelIndex, name: str, path: str):
        """Add new ContactList.
        :todo: implement setData() -> bool
        """
        i = idx.row()
        self.clm.itemUpdate(i, name, path)
        # update settings (TODO: to handmade QSettings successor)
        s = QtCore.QSettings()
        s.beginGroup("contacts")
        s.beginWriteArray("sources")
        s.setArrayIndex(i)
        s.setValue("name", name)
        s.setValue("path", path)
        s.endArray()
        s.endGroup()

    def itemDel(self, i: int):
        """Delete record #i.
        :fixme: shift higher entries to low
        :todo: implment removeRows() -> bool
        """
        self.beginRemoveRows(QtCore.QModelIndex(), i, i)
        self.clm.itemDel(i)
        self.endRemoveRows()
        # - update settings (TODO: to handmade QSettings successor)
        s = QtCore.QSettings()
        s.beginGroup("contacts")
        s.beginWriteArray("sources")
        s.setArrayIndex(i)
        s.remove("")
        s.endArray()
        s.endGroup()

    def findByName(self, s: str, i: int = None) -> bool:
        """Find existent CL by name [excluding i-th entry]
        :return: True if found
        """
        return self.clm.findByName(s, i)

    def findByPath(self, s: str, i: int = None) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        return self.clm.findByPath(s, i)
