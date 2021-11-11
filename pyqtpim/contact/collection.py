"""Contact list"""
import os
# 2. 3rd
# import magic # not works
import vobject
from PySide2 import QtCore
# 3. local
from .entry import Contact

# magic = magic.Magic()


class ContactList(list[Contact]):
    """Contact list
    :todo: lazy/async [re]load
    """
    path: str

    def __init__(self, path: str = None):
        self.path = path

    def size(self):
        return len(self)

    def print(self):
        for v in self:
            v.print()

    def load_f(self, fp: str):
        """Load entries from file
        :param fp: file path
        """
        # print(magic.from_file(fp))
        with open(fp, 'rt') as stream:
            for v in vobject.readComponents(stream):
                if v.name == 'VCARD':
                    self.append(Contact(v))

    def reload(self):
        """Load entries from dir"""
        with os.scandir(self.path) as itr:
            for entry in itr:
                if not entry.is_file():
                    continue
                self.load_f(entry.path)


class ContactListModel(QtCore.QAbstractTableModel):
    cl: ContactList

    def __init__(self, *args, cl=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cl = cl or []

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
            else:
                return ''

    def rowCount(self, index):
        return self.cl.size()

    def columnCount(self, index):
        return 3
