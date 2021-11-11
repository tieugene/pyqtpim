"""ContactListCollection"""

# 2. PySide
from PySide2 import Qt, QtCore
# 3. local
from . import collection


class ContactListManager(list[collection.ContactList]):
    def add(self, collect):
        self.append(collect)

    def print(self):
        for c in self:
            c.print()

    def reload(self):
        for c in self:
            c.reload()


class ContactListModel(QtCore.QAbstractListModel):

    def __init__(self, *args, mgr=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.mgr = mgr or []

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            c = self.mgr[index.row()]
            # Return the todo text only.
            return c.name

    def rowCount(self, index):
        return len(self.mgr)
