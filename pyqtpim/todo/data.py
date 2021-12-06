"""vToDo data provider
:todo: field type enum
"""
# 1. std
from _collections import OrderedDict
from datetime import datetime, date
from typing import Optional, Union, Any
# 2. 3rd
import vobject
# 3. local
from common import Entry, EntryList, EntryListManager
from . import enums


class Todo(Entry):
    def __init__(self, path: str, data: vobject.base.Component):
        super().__init__(path, data)
        self._name2func = {
            enums.EProp.Categories: self.getCategories,
            enums.EProp.Class: self.getClass,
            enums.EProp.Comment: self.getComment,
            enums.EProp.Completed: self.getCompleted,
            enums.EProp.Contact: self.getContact,
            enums.EProp.Created: self.getCreated,
            enums.EProp.Description: self.getDescription,
            enums.EProp.DTStamp: self.getDTStamp,
            enums.EProp.DTStart: self.getDTStart,
            enums.EProp.Due: self.getDue,
            enums.EProp.LastModified: self.getLastModified,
            enums.EProp.Location: self.getLocation,
            enums.EProp.Percent: self.getPercent,
            enums.EProp.Priority: self.getPriority,
            enums.EProp.RelatedTo: self.getRelatedTo,
            enums.EProp.RRule: self.getRRule,
            enums.EProp.Sequence: self.getSequence,
            enums.EProp.Status: self.getStatus,
            enums.EProp.Summary: self.getSummary,
            enums.EProp.UID: self.getUID,
            enums.EProp.URL: self.getURL,
        }

    def RawContent(self) -> Optional[OrderedDict]:
        """Return inner item content as structure.
        """
        retvalue: OrderedDict = OrderedDict()
        cnt = self._data.vtodo.contents
        keys = list(cnt.keys())
        keys.sort()
        for k in keys:  # v: list allways
            if k == 'valarm':   # hack
                continue
            if v := self.__getFldByName(k):
                retvalue[k] = v
        return retvalue

    def __getFldByName(self, fld: str) -> Any:
        """Get field value by its name."""
        if v_list := self._data.vtodo.contents.get(fld):
            if len(v_list) == 1:  # usual
                v = v_list[0].value
            else:  # multivalues (attach, categories etc)
                v = [i.value for i in v_list]
            return v

    def __setAFldByName(self, fld: str, data: Optional[Union[int, str, date, datetime]]):
        """Create/update standalone [optional] field"""
        if data is None:
            if fld in self._data.vtodo.contents:
                print("Del", fld, self._data.vtodo.contents[fld][0])
                del self._data.vtodo.contents[fld]
        else:
            if fld in self._data.vtodo.contents:
                print("Set", fld, ':', self._data.vtodo.contents[fld][0].value, '=>', data)
                # self._data.vtodo.<fld>>.value
                self._data.vtodo.contents[fld][0].value = data
            else:
                print("Add", fld, data)
                self._data.vtodo.add(fld).value = data

    # getters
    def getAttach(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('attach')

    def getCategories(self) -> Optional[Union[str, list[str]]]:
        """Categories.
        :return: Category:str or list of categories

        Can be:
        - None
        - ['Cat1']
        - [['Cat1'], ['Cat2'], ...]
        """
        retvalue = self.__getFldByName('categories')
        if retvalue:
            if isinstance(retvalue[0], str):
                retvalue = retvalue[0]
            else:
                retvalue = [s[0] for s in retvalue]
                retvalue.sort()
        return retvalue

    def getClass(self) -> Optional[enums.EClass]:
        if v := self.__getFldByName('class'):
            return enums.Raw2Enum_Class.get(v)

    def getComment(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('comment')

    def getCompleted(self) -> Optional[datetime]:
        return self.__getFldByName('completed')

    def getContact(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('contact')

    def getCreated(self) -> Optional[datetime]:
        return self.__getFldByName('created')

    def getDescription(self) -> Optional[str]:
        return self.__getFldByName('description')

    def getDTStamp(self) -> datetime:
        return self.__getFldByName('dtstamp')

    def getDTStart(self) -> Optional[Union[date, datetime]]:
        return self.__getFldByName('dtstart')

    def getDue(self) -> Optional[Union[date, datetime]]:
        return self.__getFldByName('due')

    def getLastModified(self) -> Optional[datetime]:
        return self.__getFldByName('last-modified')

    def getLocation(self) -> Optional[str]:
        return self.__getFldByName('location')

    def getPercent(self) -> Optional[int]:
        if v := self.__getFldByName('percent-complete'):
            return int(v)

    def getPriority(self) -> Optional[int]:
        """
        0=undef, 1[..4]=high, 5=mid, [6..]9=low
        :return: 1[/3]/5[/7]/9

        cases: (164):
        - 1=18
        - 3=6
        - 5=58
        - 7=6
        - 9=76
        """
        if v := self.__getFldByName('priority'):
            return int(v)

    def getRelatedTo(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('related-to')

    def getRRule(self) -> Optional[str]:
        return self.__getFldByName('rrule')

    def getSequence(self) -> Optional[int]:
        if v := self.__getFldByName('sequence'):
            return int(v)

    def getStatus(self) -> Optional[enums.EStatus]:
        if v := self.__getFldByName('status'):
            return enums.Raw2Enum_Status.get(v)

    def getSummary(self) -> Optional[str]:
        # return self._data.vtodo.summary.value
        return self.__getFldByName('summary')

    def getUID(self) -> str:
        return self.__getFldByName('uid')

    def getURL(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('url')

    # setters (TODO: chg to 'tryupdate')
    # - cat
    def setClass(self, data: Optional[enums.EClass]):
        self.__setAFldByName('class', enums.Enum2Raw_Class.get(data))

    def setCompleted(self, data: Optional[Union[date, datetime]]):
        self.__setAFldByName('completed', data)

    def setDescription(self, data: Optional[str]):
        self.__setAFldByName('description', data)

    def setDTStart(self, data: Optional[Union[date, datetime]]):
        self.__setAFldByName('dtstart', data)

    def setDue(self, data: Optional[Union[date, datetime]]):
        self.__setAFldByName('due', data)

    def setLocation(self, data: Optional[str]):
        self.__setAFldByName('location', data)

    def setPercent(self, data: Optional[int]):
        self.__setAFldByName('percent-complete', data)

    def setPriority(self, data: Optional[int]):
        self.__setAFldByName('priority', data)

    def setStatus(self, data: Optional[enums.EStatus]):
        self.__setAFldByName('status', enums.Enum2Raw_Status.get(data))

    def setSummary(self, data: Optional[str]):
        self.__setAFldByName('summary', data)

    def setURL(self, data: Optional[str]):
        self.__setAFldByName('url', data)

    # misc
    def serialize(self) -> str:
        return self._data.serialize()


class TodoList(EntryList):
    """todo: collect categories/locations on load"""
    def _load_one(self, fname: str, data: vobject.base.Component):
        if data.name == 'VCALENDAR' and 'vtodo' in data.contents:
            self._data.append(Todo(fname, data))


class TodoListManager(EntryListManager):
    def itemAdd(self, name: str, path: str):
        self.append(TodoList(name, path))
