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
        return self.cl.size()

    def columnCount(self, index):
        return 5

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
        return self.count

    # self
    def __init_data(self):
        """:todo: lazy load"""
        for name, path in ABs:
            cl = ContactList(path)
            cl.load()
            self.clm.add(name, cl)

    def add(self, name: str, path: str):
        """Add new ContactList"""
        count = self.clm.size()
        self.beginInsertRows(QtCore.QModelIndex(), count, count)
        cl = ContactList(path)
        cl.load()
        self.clm.add(name, cl)
        self.endInsertRows()
        # save to settings
        s = QtCore.QSettings()
        s.beginGroup("contacts")
        s.beginWriteArray("sources")
        s.setArrayIndex(count)
        s.setValue("name", name)
        s.setValue("path", path)
        s.endArray()
        s.endGroup()

    def findByName(self, s: str) -> bool:
        """Find existent CL by name
        :return: True if found
        """
        return self.clm.findByName(s)

    def findByPath(self, s: str) -> bool:
        """Find existent CL by path
        :return: True if found
        """
        return self.clm.findByPath(s)

    @property
    def count(self):
        return self.clm.size()
