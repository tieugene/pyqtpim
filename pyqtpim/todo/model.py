# 1. system
from typing import Any
# 2. PySide
from PySide2 import QtCore
# 3. local
from common import SetGroup, EntryListModel, EntryListManagerModel
from .data import TodoList, TodoListManager
from . import enums


class TodoListModel(EntryListModel):
    __types = set()  # temp types cache
    __DemapClass = {
        enums.EClass.Public: "Do something",
        enums.EClass.Private: "wait...",
        enums.EClass.Confidential: "OK"
    }
    __DemapStatus = {
        enums.EStatus.NeedsAction: "Do something",
        enums.EStatus.InProcess: "wait...",
        enums.EStatus.Completed: "OK",
        enums.EStatus.Cancelled: "WontFix",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._data = TodoList()
        self.setTable("entry")
        self.setHeaderData(self.fieldIndex('id'), QtCore.Qt.Horizontal, 'ID')
        self.setHeaderData(self.fieldIndex('store_id'), QtCore.Qt.Horizontal, 'store')
        self.setHeaderData(self.fieldIndex('created'), QtCore.Qt.Horizontal, "Created")
        self.setHeaderData(self.fieldIndex('modified'), QtCore.Qt.Horizontal, "Updated")
        self.setHeaderData(self.fieldIndex('dtstart'), QtCore.Qt.Horizontal, "DTStart")
        self.setHeaderData(self.fieldIndex('due'), QtCore.Qt.Horizontal, "Due")
        self.setHeaderData(self.fieldIndex('completed'), QtCore.Qt.Horizontal, "Completed")
        self.setHeaderData(self.fieldIndex('progress'), QtCore.Qt.Horizontal, "%")
        self.setHeaderData(self.fieldIndex('priority'), QtCore.Qt.Horizontal, "Prio")
        self.setHeaderData(self.fieldIndex('status'), QtCore.Qt.Horizontal, "Status")
        self.setHeaderData(self.fieldIndex('summary'), QtCore.Qt.Horizontal, "Summary")
        self.setHeaderData(self.fieldIndex('location'), QtCore.Qt.Horizontal, "Loc")
        self.setHeaderData(self.fieldIndex('body'), QtCore.Qt.Horizontal, "Body")
        self.select()

    # def _empty_item(self) -> TodoList:
    #    return TodoList()

    # def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
    #     """
    #
    #     :param index:
    #     :param role:
    #     :return:
    #
    #     Types from uplink:
    #     - NoneType
    #     - int
    #     - str
    #     - PySide2.QtCore.QDate
    #     - PySide2.QtCore.QDateTime
    #     - EClass
    #     - EStatus
    #     """
    #     def __chk_type(_v: Any):
    #         t = type(_v)
    #         if t not in self.__types:
    #             self.__types.add(t)
    #             print(t)
    #     v = super().data(index, role)
    #     # __chk_type(v)
    #     # FIXME: too dumb selection
    #     if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:  # list/details
    #         if isinstance(v, enums.EClass):
    #             v = self.__DemapClass[v]
    #         elif isinstance(v, enums.EStatus):
    #             v = self.__DemapStatus[v]
    #         elif isinstance(v, list):
    #             if role == QtCore.Qt.DisplayRole:
    #                 v = ', '.join(v)
    #             else:
    #                 v = '\n'.join(v)
    #     return v


class TodoListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo
        # self._data = TodoListManager()
        # self._init_data()
