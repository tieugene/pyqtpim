"""PySide interface"""

# 2. PySide
import typing

from PySide2 import QtCore
# 3. local
from .collection import ContactList, ContactListManager

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

    def __init__(self, *args, cl: ContactList = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cl = cl or ContactList()

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

    def __init__(self, *args, mgr: ContactListManager = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.clm = mgr or ContactListManager()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            name, _ = self.clm[index.row()]
            return name

    def rowCount(self, index):
        return self.clm.size()
