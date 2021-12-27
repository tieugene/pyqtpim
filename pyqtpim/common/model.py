"""vCard/iCal models parents"""

# 1. system
from typing import Any
# 2. PySide
from PySide2 import QtCore
# 3. local
from . import enums
from .data import StoreList
from .settings import MySettings


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
    _set_group: enums.SetGroup
    _data_cls: type
    _data: StoreList
    activeChanged: QtCore.Signal = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Inherit
    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:
        return self._data.size()

    def flags(self, index):
        fl = QtCore.QStringListModel.flags(self, index)
        fl |= QtCore.Qt.ItemIsUserCheckable
        return fl

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return self._data.store(index.row()).name
        elif role == QtCore.Qt.CheckStateRole:
            return QtCore.Qt.Checked if self._data.store(index.row()).active else QtCore.Qt.Unchecked

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.CheckStateRole:
            row = index.row()
            self._data.store(row).active = (value == QtCore.Qt.Checked)
            self.save()
            # TODO: refresh EntryList
            # self.dataChanged.emit(index, index, (role,))
            # self.activeChanged.emit()
            return True
        return False

    # Hand-made
    def load(self):
        """Load _data from settings"""
        self._data.from_list(MySettings.get(self._set_group, 'store'))

    def save(self):
        """Save _data to settings"""
        MySettings.set(self._set_group, 'store', self._data.to_list())
