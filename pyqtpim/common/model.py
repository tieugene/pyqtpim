"""vCard/iCal models parents"""

# 1. system
from typing import Any
# 2. PySide
from PySide2 import QtCore
# 3. local
# from .settings import SetGroup
from .data import StoreList
# from . import enums


class EntryModel(QtCore.QAbstractTableModel):
    store_name = dict()  # class-wide cache of Store names (id:name)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Inherit
    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:
        return 0  # FIXME: stub

    def columnCount(self, parent: QtCore.QModelIndex = None) -> int:
        return 0  # FIXME: stub


class EntryProxyModel(QtCore.QSortFilterProxyModel):
    _own_model = EntryModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSourceModel(self._own_model(self))


class StoreModel(QtCore.QStringListModel):
    activeChanged: QtCore.Signal = QtCore.Signal()
    _data: StoreList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Inherit
    def flags(self, index):
        fl = QtCore.QStringListModel.flags(self, index)
        fl |= QtCore.Qt.ItemIsUserCheckable
        return fl

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return self._data.store(index.row()).name
        elif role == QtCore.Qt.CheckStateRole:
            return (QtCore.Qt.Unchecked, QtCore.Qt.Checked)[int(self._data.store(index.row()).active)]
