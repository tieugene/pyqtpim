"""vToDo data provider
:todo: field type enum
"""
# 1. std
import uuid
from _collections import OrderedDict
import datetime
from typing import Optional, Union, Any
# 2. 3rd
import vobject
# 3. local
from common import VObj, EntryList, EntryListManager
from . import enums


class VObjTodo(VObj):
    """In-memory one-file VTODO"""
    def __init__(self, data: vobject.base.Component = None):
        if data is None:
            uid = uuid.uuid4()
            stamp = datetime.datetime.now(tz=vobject.icalendar.utc)
            data = vobject.iCalendar()
            data.add('prodid').value = '+//IDN eap.su//NONSGML pyqtpim//EN'
            data.add('vtodo')
            data.vtodo.add('uid').value = str(uid)
            data.vtodo.add('dtstamp').value = stamp
            data.vtodo.add('created').value = stamp
        super().__init__(data)
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

    def save(self):
        self.updateStamps()
        # super().save()

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
            else:  # multivalues (unwrap; attach, categories etc)
                v = [i.value for i in v_list]
            return v

    def __setFldByName(self, fld: str, data: Optional[Union[int, str, datetime.date, datetime.datetime, list]]):
        """Create/update standalone [optional] field"""
        if isinstance(data, list):
            if fld in self._data.vtodo.contents:
                del self._data.vtodo.contents[fld]
            for v in data:
                self._data.vtodo.add(fld).value = [v]   # one cat per property recommended
        else:
            if data is None:
                if fld in self._data.vtodo.contents:
                    # print("Del", fld, self._data.vtodo.contents[fld][0])
                    del self._data.vtodo.contents[fld]
            else:
                if fld in self._data.vtodo.contents:
                    # print("Set", fld, ':', self._data.vtodo.contents[fld][0].value, '=>', data)
                    # self._data.vtodo.<fld>>.value
                    self._data.vtodo.contents[fld][0].value = data
                else:
                    # print("Add", fld, data)
                    self._data.vtodo.add(fld).value = data

    # getters
    def getAttach(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('attach')

    def getCategories(self) -> Optional[Union[str, list[str]]]:
        """Categories.
        :return: list of str
        Can be:
        - None
        - ['Cat1']
        - ['Cat1', 'Cat2', ...] (TB, not advised)
        - [['Cat1'], ['Cat2'], ...] (Evolution)
        """
        retvalue = self.__getFldByName('categories')
        if retvalue:
            if isinstance(retvalue[0], list):   # additional unwrap
                retvalue = [s[0] for s in retvalue]
        return retvalue

    def getClass(self) -> Optional[enums.EClass]:
        if v := self.__getFldByName('class'):
            return enums.Raw2Enum_Class.get(v)

    def getComment(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('comment')

    def getCompleted(self) -> Optional[datetime.datetime]:
        return self.__getFldByName('completed')

    def getContact(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('contact')

    def getCreated(self) -> Optional[datetime.datetime]:
        return self.__getFldByName('created')

    def getDescription(self) -> Optional[str]:
        return self.__getFldByName('description')

    def getDTStamp(self) -> datetime.datetime:
        return self.__getFldByName('dtstamp')

    def getDTStart(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        return self.__getFldByName('dtstart')

    def getDue(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        return self.__getFldByName('due')

    def getLastModified(self) -> Optional[datetime.datetime]:
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
    def setCategories(self, data: Optional[list[str]]):
        # print("setCategories:", data)
        self.__setFldByName('categories', data)

    def setClass(self, data: Optional[enums.EClass]):
        self.__setFldByName('class', enums.Enum2Raw_Class.get(data))

    def setCompleted(self, data: Optional[Union[datetime.date, datetime.datetime]]):
        self.__setFldByName('completed', data)

    def setDescription(self, data: Optional[str]):
        self.__setFldByName('description', data)

    def setDTStart(self, data: Optional[Union[datetime.date, datetime.datetime]]):
        self.__setFldByName('dtstart', data)

    def setDue(self, data: Optional[Union[datetime.date, datetime.datetime]]):
        self.__setFldByName('due', data)

    def setLocation(self, data: Optional[str]):
        self.__setFldByName('location', data)

    def setPercent(self, data: Optional[int]):
        self.__setFldByName('percent-complete', data)

    def setPriority(self, data: Optional[int]):
        self.__setFldByName('priority', data)

    def setStatus(self, data: Optional[enums.EStatus]):
        self.__setFldByName('status', enums.Enum2Raw_Status.get(data))

    def setSummary(self, data: Optional[str]):
        self.__setFldByName('summary', data)

    def setURL(self, data: Optional[str]):
        self.__setFldByName('url', data)

    # specials
    def updateStamps(self):
        seq = 0 if (seq := self.getSequence()) is None else seq + 1
        self.__setFldByName('sequence', str(seq))
        utc = vobject.icalendar.utc
        self.__setFldByName('last-modified', datetime.datetime.now(tz=utc))


class TodoList(EntryList):
    """todo: collect categories/locations on load"""
    def _load_one(self, fpath: str, data: vobject.base.Component):
        if data.name == 'VCALENDAR' and 'vtodo' in data.contents:
            self._data.append(VObjTodo(data))

    def _mkItem(self):
        return VObjTodo(self.path)


class TodoListManager(EntryListManager):
    """todo: del"""
    def itemAdd(self, name: str, path: str):
        self.append(TodoList(name, path))
