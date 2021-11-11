"""PySide interface"""

# 2. PySide
from PySide2 import QtCore
# 3. local
from .collection import ContactList, ContactListManager


class ContactListModel(QtCore.QAbstractTableModel):
    cl: ContactList

    def __init__(self, *args, cl: ContactList=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cl = cl or ContactList()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            c = self.cl[index.row()]
            col = index.column()
            if col == 0:
                return c.getFN()
            elif col == 1:
                return c.getFamily()
            elif col == 2:
                return c.getGiven()
            elif col == 3:
                return c.getEmail()
            elif col == 4:
                return c.getTel()
            else:
                return ''

    def rowCount(self, index):
        return self.cl.size()

    def columnCount(self, index):
        return 5


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
