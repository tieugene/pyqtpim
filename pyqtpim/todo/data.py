"""vToDo data provider"""

# 2. 3rd
import vobject
# 3. local
from common import exc, Entry, EntryList, EntryListManager


class Todo(Entry):
    def __init__(self, path: str, data: vobject.base.Component):
        super().__init__(path, data)
        self._name2func = {
            'summary': self.getSummary
        }

    def getSummary(self) -> str:
        return self._data.summary.value


class TodoList(EntryList):
    def _load_one(self, fname: str, data: vobject.base.Component):
        if data.name == 'VCALENDAR':
            if 'vtodo' in data.contents:
                self._data.append(Todo(fname, data.vtodo))
            # else:  # has no VTODO
        # else:
        #    raise exc.EntryLoadError(f"It is not VCALENDAR: {fname}={data.name}")


class TodoListManager(EntryListManager):
    def itemAdd(self, name: str, path: str):
        self.append(TodoList(name, path))
