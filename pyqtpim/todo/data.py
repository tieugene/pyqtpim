"""vToDo data provider
:todo: field type enum
"""
# 1. std
from _collections import OrderedDict
from datetime import datetime, date
from typing import Optional, Union
# 2. 3rd
import vobject
# 3. local
from common import Entry, EntryList, EntryListManager
from . import enums


class Todo(Entry):
    __MapClass = {
        'PUBLIC': enums.EClass.Public,
        'PRIVATE': enums.EClass.Private,
        'CONFIDENTIAL': enums.EClass.Confidential
    }
    __MapStatus = {
        'NEEDS-ACTION': enums.EStatus.NeedsAction,
        'IN-PROCESS': enums.EStatus.InProcess,
        'COMPLETED': enums.EStatus.Completed,
        'CANCELLED': enums.EStatus.Cancelled
    }
    __MapTrans = {
        'OPAQUE': enums.ETrans.Opaque,
        'TRANSPARENT': enums.ETrans.Transparent
    }

    def __init__(self, path: str, data: vobject.base.Component):
        super().__init__(path, data)
        self._name2func = {
            'categories': self.getCategories,
            'class': self.getClass,
            'completed': self.getCompleted,
            'dtstart': self.getDTStart,
            'due': self.getDue,
            'location': self.getLocation,
            'percent': self.getPercent,
            'priority': self.getPriority,
            'status': self.getStatus,
            'summary': self.getSummary,
            'transparency': self.getTrans
        }

    def RawContent(self) -> Optional[OrderedDict]:
        """Return inner item content as structure"""
        retvalue: OrderedDict = OrderedDict()
        cnt = self._data.contents
        keys = list(cnt.keys())
        keys.sort()
        for k in keys:  # v: list allways
            if k == 'valarm':   # hack
                continue
            if v := self.__getFldByName(k):
                retvalue[k] = v
        return retvalue

    def __getFldByName(self, fld: str) -> Optional[Union[str, list]]:
        if v_list := self._data.contents.get(fld):
            if len(v_list) == 1:  # usual
                v = v_list[0].value
            else:  # multivalues (attach, categories)
                v = [i.value for i in v_list]
            return v

    # for model
    def getCategories(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('categories')

    def getClass(self) -> Optional[enums.EClass]:
        if v := self.__getFldByName('class'):
            return self.__MapClass.get(v)

    def getCompleted(self) -> Optional[datetime]:
        return self.__getFldByName('completed')

    def getDTStart(self) -> Optional[Union[date, datetime]]:
        return self.__getFldByName('dtstart')   # TODO: date[time]

    def getDue(self) -> Optional[Union[date, datetime]]:
        return self.__getFldByName('due')       # TODO: date[time]

    def getLocation(self) -> Optional[str]:
        return self.__getFldByName('location')

    def getPercent(self) -> Optional[int]:
        if v := self.__getFldByName('percent-complete'):
            return int(v)

    def getPriority(self) -> Optional[int]:
        if v := self.__getFldByName('priority'):
            return int(v)

    def getStatus(self) -> Optional[enums.EStatus]:
        if v := self.__getFldByName('status'):
            return self.__MapStatus.get(v)

    def getSummary(self) -> str:
        return self._data.summary.value

    def getTrans(self) -> Optional[enums.ETrans]:
        if v := self.__getFldByName('transparency'):
            return self.__MapTrans.get(v)
    # /for model


class TodoList(EntryList):
    def _load_one(self, fname: str, data: vobject.base.Component):
        if data.name == 'VCALENDAR':
            if 'vtodo' in data.contents:
                self._data.append(Todo(fname, data.vtodo))


class TodoListManager(EntryListManager):
    def itemAdd(self, name: str, path: str):
        self.append(TodoList(name, path))
