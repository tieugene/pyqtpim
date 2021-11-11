"""ContactListCollection"""

# 2. PySide
from PySide2 import QtCore
# 3. local
from . import collection


class ContactListManager(list[(str, collection.ContactList)]):

    def size(self):
        return len(self)

    def add(self, name: str, collect: collection.ContactList):
        self.append((name, collect))

    def print(self):
        for n, c in self:
            if c.size():
                print(f"==== {n} ====")
                c.print()
                print(f"==== /{n} ====")
            else:
                print(f"==== {n}/ ====")
        else:
            print("==== <empty> ====")

    def reload(self):
        for _, c in self:
            c.reload()


class ContactListManagerModel(QtCore.QAbstractListModel):
    mgr: ContactListManager

    def __init__(self, *args, mgr: ContactListManager = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.mgr = mgr or ContactListManager()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            n, c = self.mgr[index.row()]
            return n

    def rowCount(self, index):
        return self.mgr.size()
