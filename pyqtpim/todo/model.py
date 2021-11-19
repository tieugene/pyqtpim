# 1. system
# 2. PySide
from typing import Any

from PySide2 import QtCore
# 3. local
from common import SetGroup, EntryListModel, EntryListManagerModel
from .data import TodoList, TodoListManager
from . import enums


class TodoListModel(EntryListModel):
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
    __DemapTrans = {
        enums.ETrans.Opaque: "Too busy",
        enums.ETrans.Transparent: "Welcome"
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
            ("Trans", 'transparency'),
        )

    def _empty_item(self) -> TodoList:
        return TodoList()

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        v = super().data(index, role)
        if isinstance(v, enums.EClass):     # FIXME: too dumb selection
            v = self.__DemapClass[v]
        elif isinstance(v, enums.EStatus):
            v = self.__DemapStatus[v]
        elif isinstance(v, enums.ETrans):
            v = self.__DemapTrans[v]
        return v


class TodoListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo
        self._data = TodoListManager()
        self._init_data()
