"""vToDo data provider
:todo: field type enum
"""
# 1. std
import uuid
import datetime
from _collections import OrderedDict
from typing import Optional, Union, Any, Callable
from functools import wraps
# 2. 3rd
import vobject
# 3. local
from common import VObj
from . import enums


def _utcnow():
    return datetime.datetime.now(tz=vobject.icalendar.utc).replace(microsecond=0)


def get_X(name: str):
    """Decorate getter"""
    def get_decorator(func):
        @wraps(func)
        def wrapper(self):
            if name in self._data.vtodo.contents:
                return func(self)
        return wrapper
    return get_decorator


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
    @get_X('attach')
    def get_Attach(self) -> list[str]:
        return self._data.vtodo.attach.value   # attach_list?

    @get_X('categories')
    def get_Categories(self) -> Union[str, list[str]]:
        """Categories.
        :return: list of str
        Can be:
        - None
        - ['Cat1']
        - ['Cat1', 'Cat2', ...] (TB, not advised)
        - [['Cat1'], ['Cat2'], ...] (Evolution)
        """
        retvalue = self._data.vtodo.categories.value  # :list
        # print("Cat:", retvalue, type(retvalue))
        if isinstance(retvalue[0], list):   # additional unwrap
            retvalue = [s[0] for s in retvalue]
        return retvalue

    @get_X('class')
    def get_Class(self) -> enums.EClass:
        return enums.Raw2Enum_Class.get(self._data.vtodo.contents['class'][0].value)    # FIXME:

    @get_X('comment')
    def get_Comment(self) -> Optional[Union[str, list[str]]]:
        return self._data.vtodo.comment.value   # comment_list?

    @get_X('completed')
    def get_Completed(self) -> datetime.datetime:
        return self._data.vtodo.completed.value

    @get_X('contact')
    def get_Contact(self) -> Union[str, list[str]]:
        return self._data.vtodo.contact.value   # contact_list?

    @get_X('created')
    def get_Created(self) -> datetime.datetime:
        return self._data.vtodo.created.value

    @get_X('description')
    def get_Description(self) -> str:
        return self._data.vtodo.description.value

    @get_X('dtstamp')
    def get_DTStamp(self) -> datetime.datetime:
        return self._data.vtodo.dtstamp.value

    @get_X('dtstart')
    def get_DTStart(self) -> Union[datetime.date, datetime.datetime]:
        return self._data.vtodo.dtstart.value

    @get_X('due')
    def get_Due(self) -> Union[datetime.date, datetime.datetime]:
        return self._data.vtodo.due.value

    @get_X('due')
    def get_Due_as_date(self) -> datetime.date:
        return v.date() if isinstance(v := self._data.vtodo.due.value, datetime.datetime) else v

    @get_X('last-modified')
    def get_LastModified(self) -> datetime.datetime:
        return self._data.vtodo.last_modified.value

    @get_X('location')
    def get_Location(self) -> str:
        return self._data.vtodo.location.value

    @get_X('percent-complete')
    def get_Progress(self) -> int:
        return int(self._data.vtodo.percent_complete.value)

    @get_X('priority')
    def get_Priority(self) -> int:
        """
        0=undef, 1[..4]=high, 5=mid, [6..]9=low
        :return: 1[/3]/5[/7]/9

        cases: (164): 1=18, 3=6, 5=58, 7=6, 9=76
        """
        return int(self._data.vtodo.priority.value)

    @get_X('related-to')
    def get_RelatedTo(self) -> Union[str, list[str]]:
        return self._data.vtodo.related_to_list.value

    @get_X('rrule')
    def get_RRule(self) -> str:
        return self._data.vtodo.rrule.value

    @get_X('sequence')
    def get_Sequence(self) -> int:
        return int(self._data.vtodo.sequence.value)

    @get_X('status')
    def get_Status(self) -> enums.EStatus:
        return enums.Raw2Enum_Status.get(self._data.vtodo.status.value)

    @get_X('summary')
    def get_Summary(self) -> str:
        return self._data.vtodo.summary.value

    @get_X('uid')
    def get_UID(self) -> str:
        return self._data.vtodo.uid.value

    @get_X('url')
    def get_URL(self) -> str:
        # return self._data.vtodo.url.value if 'url' in self._data.vtodo.contents else None
        return self._data.vtodo.url.value

    # setters (TODO: chg to 'tryupdate')
    def set_Categories(self, data: Optional[list[str]]):
        # print("setCategories:", data)
        self.__setFldByName('categories', data)

    def set_Class(self, data: Optional[enums.EClass]):
        self.__setFldByName('class', enums.Enum2Raw_Class.get(data))

    def set_Completed(self, data: Optional[Union[datetime.date, datetime.datetime]]):
        self.__setFldByName('completed', data)

    def set_Description(self, data: Optional[str]):
        self.__setFldByName('description', data)

    def set_DTStart(self, data: Optional[Union[datetime.date, datetime.datetime]]):
        # Workaround https://github.com/eventable/vobject/issues/180
        # print("setDTStart:", data, type(data))
        self.__setFldByName('dtstart', data, force=True)

    def set_Due(self, data: Optional[Union[datetime.date, datetime.datetime]]):
        # Workaround
        self.__setFldByName('due', data, force=True)

    def set_Location(self, data: Optional[str]):
        self.__setFldByName('location', data)

    def set_Progress(self, data: Optional[int]):
        self.__setFldByName('percent-complete', str(data))  # https://github.com/eventable/vobject/issues/178

    def set_Priority(self, data: Optional[int]):
        self.__setFldByName('priority', str(data))  # https://github.com/eventable/vobject/issues/178

    def set_Status(self, data: Optional[enums.EStatus]):
        self.__setFldByName('status', enums.Enum2Raw_Status.get(data))

    def set_Summary(self, data: Optional[str]):
        self.__setFldByName('summary', data)

    def set_URL(self, data: Optional[str]):
        self.__setFldByName('url', data)

    # misc
    def updateStamps(self):
        seq = 0 if (seq := self.get_Sequence()) is None else seq + 1
        self.__setFldByName('sequence', str(seq))  # https://github.com/eventable/vobject/issues/178
        now = _utcnow()
        self.__setFldByName('last-modified', now)
        self.__setFldByName('dtstamp', now)
