"""PySide interface"""

# 1. system
import typing
# 2. PySide
from PySide2 import QtCore
# 3. local
from common.model import EntryListManagerModel
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
    __data: ContactList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__data = ContactList()

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> typing.Any:
        """TODO: use setHeaderData() in __init__()"""
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.DisplayRole:
            return FIELD_NAMES[section][0]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:  # EditRole for mapper
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


class ContactListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = 'contacts'
        self._data = ContactListManager()
        self._init_data()
