# 1. system
# 2. PySide
from typing import Any

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
        self._data = TodoList()
        self._fld_names = (
            ("Summary", 'summary'),
            ("Class", 'class'),
            ("Completed", 'completed'),
            ("DTStart", 'dtstart'),
            ("Due", 'due'),
            ("%", 'percent'),
            ("Prio", 'priority'),
            ("Status", 'status'),
            ("Loc", 'location'),
            ("Cat", 'categories'),
        )

    def _empty_item(self) -> TodoList:
        return TodoList()

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        """

        :param index:
        :param role:
        :return:

        Types from uplink:
        - NoneType
        - int
        - str
        - PySide2.QtCore.QDate
        - PySide2.QtCore.QDateTime
        - EClass
        - EStatus
        """
        def __chk_type(v: Any):
            t = type(v)
            if t not in self.__types:
                self.__types.add(t)
                print(t)
        v = super().data(index, role)
        # __chk_type(v)
        # FIXME: too dumb selection
        if isinstance(v, enums.EClass):
            v = self.__DemapClass[v]
        elif isinstance(v, enums.EStatus):
            v = self.__DemapStatus[v]
        elif isinstance(v, list):
            if role == QtCore.Qt.DisplayRole:
                v = ', '.join(v)
            elif role == QtCore.Qt.EditRole:
                v = '\n'.join(v)
        return v


class TodoListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo
        self._data = TodoListManager()
        self._init_data()
