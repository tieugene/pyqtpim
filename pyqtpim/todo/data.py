"""vToDo data provider"""

# 2. 3rd
from _collections import OrderedDict

import vobject
# 3. local
from common import Entry, EntryList, EntryListManager


class Todo(Entry):
    def __init__(self, path: str, data: vobject.base.Component):
        super().__init__(path, data)
        self._name2func = {
            'summary': self.getSummary
        }

    def getSummary(self) -> str:
        return self._data.summary.value

    def getContent(self) -> OrderedDict:
        """Return inner item content as structure"""
        retvalue: OrderedDict = OrderedDict()
        cnt = self._data.contents
        keys = list(cnt.keys())
        keys.sort()
        for k in keys:  # v: list allways
            if k == 'valarm':   # hack
                continue
            v_list = cnt[k]
            if len(v_list) == 1:    # usual
                v = v_list[0].value
            else:                   # multivalues (attach, categories)
                v = [i.value for i in v_list]
            retvalue[k] = v
        return retvalue


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
