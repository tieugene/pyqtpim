# 1. system
# 2. PySide
from PySide2 import QtCore
# 3. local
from common import SetGroup, EntryListModel, EntryListManagerModel
from .data import TodoList, TodoListManager


class TodoListModel(EntryListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = TodoList()
        self._fld_names = (
            ("Summary", 'summary'),
            ("Completed", 'completed'),
            ("DTStart", 'dtstart'),
            ("Due", 'due'),
            ("%", 'percent'),
            ("Prio", 'priority'),
            ("Status", 'status'),
        )

    def _empty_item(self) -> TodoList:
        return TodoList()


class TodoListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo
        self._data = TodoListManager()
        self._init_data()
