# 1. system
# 2. PySide
from typing import Any

from PySide2 import QtCore, QtSql
# 3. local
from .settings import MySettings, SetGroup


class EntryModel(QtSql.QSqlTableModel):
    # _data: EntryList
    # _fld_names: tuple[tuple[IntEnum, str]]  # FIXME:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
    #     """TODO: use setHeaderData() in __init__()"""
    #     if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.DisplayRole:
    #         return self._fld_names[section][1]
    #     return super().headerData(section, orientation, role)

    # def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
    #     if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:  # EditRole for mapper
    #         c = self._data.item(index.row())
    #         col = index.column()
    #         v = c.getPropByName(self._fld_names[col][0])
    #         if isinstance(v, datetime.datetime):
    #             v = QtCore.QDateTime(v)
    #         elif isinstance(v, datetime.date):
    #             v = QtCore.QDate(v)
    #         return v

    # def columnCount(self, _: QtCore.QModelIndex = None) -> int:
    #     return len(self._fld_names)

    # def rowCount(self, index: QtCore.QModelIndex = None) -> int:
    #     return self.size

    # def insertRows(self, row: int, count: int, parent: QtCore.QModelIndex = None) -> bool:
    #     self.beginInsertRows(parent, row, row+count-1)
    #     self._data.insert(row, count)
    #     self.endInsertRows()
    #     return True

    # def removeRows(self, row: int, count: int, parent: QtCore.QModelIndex = None) -> bool:
    #     self.beginRemoveRows(parent, row, row+count-1)
    #     self._data.remove(row, count)
    #     self.endRemoveRows()
    #     return True

    # self
    # @property
    # def size(self) -> int:
    #     return self._data.size

    # @property
    # def path(self) -> str:
    #     return self._data.path

    # def _empty_item(self) -> EntryList:
    #     print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")
    #     return EntryList()

    # def switch_data(self, new_el: EntryList = None):
    #     self.beginResetModel()
    #     self._data = new_el or self._empty_item()
    #     self.endResetModel()

    # def item(self, i: int) -> Entry:
    #     return self._data.item(i)


class StoreModel(QtSql.QSqlTableModel):
    activeChanged: QtCore.Signal = QtCore.Signal()  #
    _set_group: SetGroup

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable("store")
        self.setSort(self.fieldIndex('id'), QtCore.Qt.SortOrder.AscendingOrder)
        self.setHeaderData(self.fieldIndex('id'), QtCore.Qt.Horizontal, 'ID')
        self.setHeaderData(self.fieldIndex('active'), QtCore.Qt.Horizontal, '✓')
        self.setHeaderData(self.fieldIndex('name'), QtCore.Qt.Horizontal, "Name")
        self.setHeaderData(self.fieldIndex('connection'), QtCore.Qt.Horizontal, "Connection")
        self.select()

    # Inherited
    def flags(self, index):
        fl = QtSql.QSqlTableModel.flags(self, index)
        if index.column() == self.fieldIndex('name'):
            fl |= QtCore.Qt.ItemIsUserCheckable
        return fl

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole) -> Any:
        if role == QtCore.Qt.CheckStateRole \
                and (self.flags(index) & QtCore.Qt.ItemIsUserCheckable != QtCore.Qt.NoItemFlags):
            return QtCore.Qt.Checked if bool(self.data(index.siblingAtColumn(self.fieldIndex('active')))) \
                    else QtCore.Qt.Unchecked
        else:
            return QtSql.QSqlTableModel.data(self, index, role)

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.CheckStateRole and \
                (self.flags(index) & QtCore.Qt.ItemIsUserCheckable != QtCore.Qt.NoItemFlags):
            # value = QtCore.Qt.Unchecked=0 | QtCore.Qt.Checked=2
            self.setData(index.siblingAtColumn(self.fieldIndex('active')), 1 if value == QtCore.Qt.Checked else 0)
            self.submit()
            # self.dataChanged.emit(index, index, (role,))
            self.activeChanged.emit()
            return True
        return QtSql.QSqlTableModel.setData(self, index, value, role)

    # Hand-made
