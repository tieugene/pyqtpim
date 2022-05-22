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
from pym_core.base.data import VObj, Entry, EntryList, Store, StoreList
from . import enums


def _utcnow():
    return datetime.datetime.now(tz=vobject.icalendar.utc).replace(microsecond=0)


def get_X(name: str):
    """Decorate getter
    :param name: Attribute name in vobject
    """
    def get_decorator(func: Callable):
        @wraps(func)
        def wrapper(self):
            if name in self._data.vtodo.contents:
                return func(self)
        return wrapper
    return get_decorator


def set_X(name: str, getter: Callable, cvt=None):
    """Decorate setter
    :param name: Attribute name in vobject
    :param getter: get_X name to get old value
    :param cvt: store new as str(new) (hack for `int` end `base.Enum2Raw_*`)
    :return: True if value changed, False if not
    """

    def set_decorator(func: Callable):
        @wraps(func)
        def wrapper(self, new: Any):
            old = getter(self)
            if old == new:
                return False
            else:
                if old is None:
                    # print("+", name, '=', new)
                    if cvt is None:
                        self._data.vtodo.add(name).value = new
                    elif isinstance(cvt, dict):
                        self._data.vtodo.add(name).value = cvt[new]
                    elif isinstance(cvt, Callable):
                        self._data.vtodo.add(name).value = cvt(new)
                    else:
                        print(f"Strange cvt '{cvt}' for '{name}'")
                        return False
                elif new is None:
                    # print("-", name, '=', old)
                    del self._data.vtodo.contents[name]
                else:
                    # print("=", name, ':', old, '>', new)
                    func(self, new)
                return True
        return wrapper
    return set_decorator


class TodoVObj(VObj):
    """In-memory one-file VTODO"""

    def __init__(self, data: Optional[vobject.base.Component] = None):
        if data is None:
            uid = uuid.uuid4()
            stamp = _utcnow()
            data = vobject.iCalendar()
            data.add('prodid').value = '+//IDN eap.su//NONSGML pym_gui//EN'
            data.add('vtodo')
            data.vtodo.add('uid').value = str(uid)
            data.vtodo.add('created').value = stamp
        super().__init__(data)

    def RawContent(self) -> Optional[OrderedDict]:
        """Return inner item content as structure.
        :todo: generator
        """

        def __getFldByName(fld: str) -> Any:
            """Get field value by its name."""
            if v_list := self._data.vtodo.contents.get(fld):
                if len(v_list) == 1:  # usual
                    __v = v_list[0].value
                else:  # multivalues (unwrap; attach, categories etc)
                    __v = [i.value for i in v_list]
                return __v

        retvalue: OrderedDict = OrderedDict()
        cnt = self._data.vtodo.contents
        keys = list(cnt.keys())
        keys.sort()
        for k in keys:  # v: list allways
            if k == 'valarm':  # hack
                continue
            if v := __getFldByName(k):
                retvalue[k] = v
        return retvalue

    # getters
    @get_X('attach')
    def get_Attach(self) -> list[str]:
        return self._data.vtodo.attach.value  # attach_list?

    @get_X('categories')
    def get_Categories(self) -> list[str]:
        """Categories.
        :return: list of str
        Can be:
        - None
        - ['Cat1']
        - ['Cat1', 'Cat2', ...] (TB, not advised)
        - [['Cat1'], ['Cat2'], ...] (Evolution)
        :todo: return set()
        """
        retvalue = [c.value for c in self._data.vtodo.categories_list]  # unpack #1
        if isinstance(retvalue[0], list):
            retvalue = [c[0] for c in retvalue]  # unpack #2
        return retvalue

    @get_X('class')
    def get_Class(self) -> enums.EClass:
        return enums.Raw2Enum_Class.get(self._data.vtodo.contents['class'][0].value)  # FIXME:

    @get_X('comment')
    def get_Comment(self) -> list[str]:
        return self._data.vtodo.comment.value  # comment_list?

    @get_X('completed')
    def get_Completed(self) -> datetime.datetime:
        return self._data.vtodo.completed.value

    @get_X('contact')
    def get_Contact(self) -> list[str]:
        return self._data.vtodo.contact.value  # contact_list?

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

    # setters
    def set_Categories(self, data: Optional[list[str]]) -> bool:
        old = self.get_Categories()
        if old is None and data is None:
            return False
        if data is None:
            del self._data.vtodo.contents['categories']
            return True
        if old is not None:
            if set(old) == set(data):
                return False
            else:
                del self._data.vtodo.contents['categories']
        for v in data:  # FIXME: add 2+ cats
            self._data.vtodo.add('categories').value = [v]  # one cat per property recommended
        return True

    @set_X('class', get_Class, enums.Enum2Raw_Class)
    def set_Class(self, data: enums.EClass):
        self._data.vtodo.contents['class'][0].value = enums.Enum2Raw_Class[data]

    @set_X('completed', get_Completed)
    def set_Completed(self, data: datetime.datetime):
        self._data.vtodo.completed.value = data

    @set_X('description', get_Description)
    def set_Description(self, data: str):
        self._data.vtodo.description.value = data

    @set_X('dtstart', get_DTStart)
    def set_DTStart(self, data: Union[datetime.date, datetime.datetime]):
        # Workaround https://github.com/eventable/vobject/issues/180
        del self._data.vtodo.dtstart
        self._data.vtodo.add('dtstart').value = data

    @set_X('due', get_Due)
    def set_Due(self, data: Union[datetime.date, datetime.datetime]):
        # Workaround https://github.com/eventable/vobject/issues/180
        del self._data.vtodo.due
        self._data.vtodo.add('due').value = data

    @set_X('location', get_Location)
    def set_Location(self, data: str):
        self._data.vtodo.location.value = data

    @set_X('percent-complete', get_Progress, str)
    def set_Progress(self, data: int):
        self._data.vtodo.percent_complete.value = str(data)  # https://github.com/eventable/vobject/issues/178

    @set_X('priority', get_Priority, str)
    def set_Priority(self, data: int):
        self._data.vtodo.priority.value = str(data)  # https://github.com/eventable/vobject/issues/178

    @set_X('status', get_Status, enums.Enum2Raw_Status)
    def set_Status(self, data: enums.EStatus):
        self._data.vtodo.status.value = enums.Enum2Raw_Status[data]

    @set_X('summary', get_Summary)
    def set_Summary(self, data: str):
        self._data.vtodo.summary.value = data

    @set_X('url', get_URL)
    def set_URL(self, data: str):
        self._data.vtodo.url.value = data

    @set_X('sequence', get_Sequence, str)
    def __set_Sequence(self, data: int):
        self._data.vtodo.sequence.value = str(data)  # https://github.com/eventable/vobject/issues/178

    @set_X('dtstamp', get_DTStamp)
    def __set_DTStamp(self, data: datetime.datetime):
        self._data.vtodo.dtstamp.value = data

    @set_X('last-modified', get_LastModified)
    def __set_LastModified(self, data: datetime.datetime):
        self._data.vtodo.last_modified.value = data

    # misc
    def updateStamps(self):
        now = _utcnow()
        self.__set_Sequence(0 if (seq := self.get_Sequence()) is None else seq + 1)
        self.__set_DTStamp(now)
        self.__set_LastModified(now)


class TodoStore(Store):
    def __init__(self, name: str, path: str, active: bool):
        super().__init__(name, path, active)
        # self.__type = EVObjType.VTodo

    def _load_one(self, entries, vobj_src: vobject.base.Component, fname: str):
        if vobj_src.name == 'VCALENDAR' and 'vtodo' in vobj_src.contents:
            vobj = TodoVObj(vobj_src)
            entries.entry_add(TodoEntry(vobj, self, fname))


class TodoEntry(Entry):
    def __init__(self, data: TodoVObj, store: TodoStore, fname: str):
        super().__init__(data, store, fname)


class TodoEntryList(EntryList):
    def __init__(self):
        super().__init__()


class TodoStoreList(StoreList):
    _item_cls = TodoStore

    def __init__(self, entries: TodoEntryList):
        super().__init__(entries)
        # self._item_cls = TodoStore  # the same
        # self._entries = entry_list


# Warning: exactly in this order: entries > stores
entry_list = TodoEntryList()
store_list = TodoStoreList(entry_list)
