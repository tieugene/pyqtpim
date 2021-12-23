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
from common import VObj
from . import enums


def _utcnow():
    return datetime.datetime.now(tz=vobject.icalendar.utc).replace(microsecond=0)


class VObjTodo(VObj):
    """In-memory one-file VTODO"""
    def __init__(self, data: vobject.base.Component = None):
        if data is None:
            uid = uuid.uuid4()
            stamp = _utcnow()
            data = vobject.iCalendar()
            data.add('prodid').value = '+//IDN eap.su//NONSGML pyqtpim//EN'
            data.add('vtodo')
            data.vtodo.add('uid').value = str(uid)
            data.vtodo.add('created').value = stamp
        super().__init__(data)
        self._name2func = {  # FIXME: static
            enums.EProp.Categories: self.get_Categories,
            enums.EProp.Class: self.get_Class,
            enums.EProp.Comment: self.get_Comment,
            enums.EProp.Completed: self.get_Completed,
            enums.EProp.Contact: self.get_Contact,
            enums.EProp.Created: self.get_Created,
            enums.EProp.Description: self.get_Description,
            enums.EProp.DTStamp: self.get_DTStamp,
            enums.EProp.DTStart: self.get_DTStart,
            enums.EProp.Due: self.get_Due,
            enums.EProp.LastModified: self.get_LastModified,
            enums.EProp.Location: self.get_Location,
            enums.EProp.Percent: self.get_Progress,
            enums.EProp.Priority: self.get_Priority,
            enums.EProp.RelatedTo: self.get_RelatedTo,
            enums.EProp.RRule: self.get_RRule,
            enums.EProp.Sequence: self.get_Sequence,
            enums.EProp.Status: self.get_Status,
            enums.EProp.Summary: self.get_Summary,
            enums.EProp.UID: self.get_UID,
            enums.EProp.URL: self.get_URL,
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

    def __setFldByName(self, fld: str, data: Any, force=False):
        """Create/update standalone [optional] field
        :param force: recreate field
        """
        if force and fld in self._data.vtodo.contents:
            del self._data.vtodo.contents[fld]
        if isinstance(data, list):
            if fld in self._data.vtodo.contents:
                del self._data.vtodo.contents[fld]
            for v in data:
                self._data.vtodo.add(fld).value = [v]   # one cat per property recommended
        else:
            if data is None:
                if fld in self._data.vtodo.contents:
                    del self._data.vtodo.contents[fld]
            else:
                if fld in self._data.vtodo.contents:
                    self._data.vtodo.contents[fld][0].value = data
                else:
                    self._data.vtodo.add(fld).value = data

    # getters
    def get_Attach(self) -> Optional[list[str]]:
        return self.__getFldByName('attach')

    def get_Categories(self) -> Optional[Union[str, list[str]]]:
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

    def get_Class(self) -> Optional[enums.EClass]:
        if v := self.__getFldByName('class'):
            return enums.Raw2Enum_Class.get(v)

    def get_Comment(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('comment')

    def get_Completed(self) -> Optional[datetime.datetime]:
        return self.__getFldByName('completed')

    def get_Contact(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('contact')

    def get_Created(self) -> Optional[datetime.datetime]:
        return self.__getFldByName('created')

    def get_Description(self) -> Optional[str]:
        return self.__getFldByName('description')

    def get_DTStamp(self) -> datetime.datetime:
        return self.__getFldByName('dtstamp')

    def get_DTStart(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        return self.__getFldByName('dtstart')

    def get_Due(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        return self.__getFldByName('due')

    def get_Due_as_date(self) -> Optional[datetime.date]:
        return retvalue.date() if isinstance(retvalue := self.get_Due(), datetime.datetime) else retvalue

    def get_LastModified(self) -> Optional[datetime.datetime]:
        return self.__getFldByName('last-modified')

    def get_Location(self) -> Optional[str]:
        return self.__getFldByName('location')

    def get_Progress(self) -> Optional[int]:
        if v := self.__getFldByName('percent-complete'):
            return int(v)

    def get_Priority(self) -> Optional[int]:
        """
        0=undef, 1[..4]=high, 5=mid, [6..]9=low
        :return: 1[/3]/5[/7]/9

        cases: (164): 1=18, 3=6, 5=58, 7=6, 9=76
        """
        if v := self.__getFldByName('priority'):
            return int(v)

    def get_RelatedTo(self) -> Optional[Union[str, list[str]]]:
        return self.__getFldByName('related-to')

    def get_RRule(self) -> Optional[str]:
        return self.__getFldByName('rrule')

    def get_Sequence(self) -> Optional[int]:
        if v := self.__getFldByName('sequence'):
            return int(v)

    def get_Status(self) -> Optional[enums.EStatus]:
        if v := self.__getFldByName('status'):
            return enums.Raw2Enum_Status.get(v)

    def get_Summary(self) -> Optional[str]:
        # return self._data.vtodo.summary.value
        return self.__getFldByName('summary')

    def get_UID(self) -> str:
        return self.__getFldByName('uid')

    def get_URL(self) -> Optional[Union[str, list[str]]]:
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
        # Workaround https://github.com/eventable/vobject/issues/180
        # print("setDTStart:", data, type(data))
        self.__setFldByName('dtstart', data, force=True)

    def setDue(self, data: Optional[Union[datetime.date, datetime.datetime]]):
        # Workaround
        self.__setFldByName('due', data, force=True)

    def setLocation(self, data: Optional[str]):
        self.__setFldByName('location', data)

    def setPercent(self, data: Optional[int]):
        self.__setFldByName('percent-complete', str(data))  # https://github.com/eventable/vobject/issues/178

    def setPriority(self, data: Optional[int]):
        self.__setFldByName('priority', str(data))  # https://github.com/eventable/vobject/issues/178

    def setStatus(self, data: Optional[enums.EStatus]):
        self.__setFldByName('status', enums.Enum2Raw_Status.get(data))

    def setSummary(self, data: Optional[str]):
        self.__setFldByName('summary', data)

    def setURL(self, data: Optional[str]):
        self.__setFldByName('url', data)

    # specials
    def updateStamps(self):
        seq = 0 if (seq := self.get_Sequence()) is None else seq + 1
        self.__setFldByName('sequence', str(seq))  # https://github.com/eventable/vobject/issues/178
        now = _utcnow()
        self.__setFldByName('last-modified', now)
        self.__setFldByName('dtstamp', now)
