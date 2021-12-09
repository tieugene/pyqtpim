"""Common vCard/iCal parents"""

# 1. std
import inspect
import os
from _collections import OrderedDict
from enum import IntEnum
from typing import Any, Optional
# 2. 3rd
import vobject
# 3. local
from . import exc


class VObj(object):
    """In-memory vobject object"""
    _data: vobject.base.Component   # loaded vobject
    _name2func: dict[IntEnum, Any]  # mapping model column name to getter

    def __init__(self, data: vobject.base.Component):
        self._data = data

    def getPropByName(self, fld_name: IntEnum) -> Any:
        if fld := self._name2func.get(fld_name):
            return fld()

    def RawContent(self) -> Optional[OrderedDict]:
        """Get entry inside as structure"""
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")
        return OrderedDict()

    def serialize(self) -> str:
        return self._data.serialize()


class EntryList(object):
    """List of Entries
    :todo: del
    """
    __path: str
    __name: str
    __ready: bool
    _data: list[VObj]

    def __init__(self, name: str = None, path: str = None):
        self.__name = name
        self.__path = path
        self.__ready = False
        self._data = []

    def _load_one(self, fpath: str, _: vobject.base.Component):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def _mkItem(self) -> VObj:
        """Create new empty item"""
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def __load(self):
        """Load entries from dir"""
        if self.__path:
            # print(f"{self.__name}: Loading from {self.__path}")
            with os.scandir(self.__path) as itr:
                for entry in itr:
                    if not entry.is_file():
                        continue
                    with open(entry.path, 'rt') as stream:
                        # TODO: chk mimetype
                        if vcard := vobject.readOne(stream):
                            self._load_one(entry.path, vcard)
                        else:
                            raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")

    def __chk_ready(self):
        if not self.__ready:
            self.__load()
            self.__ready = True

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def size(self):
        self.__chk_ready()
        return len(self._data)

    def item(self, i: int) -> VObj:
        """Get list item"""
        self.__chk_ready()
        return self._data[i]

    def update(self, name: str, path: str):
        self.__name = name
        if path != self.__path:
            self._data.clear()
            self.__path = path
            self.__ready = False

    def insert(self, start: int, count: int):
        """Handle: 0+: insert(), rowCount+: append()"""
        for _ in range(count):
            self._data.insert(start, self._mkItem())

    def remove(self, start: int, count: int):
        """Delete 'count' entries starting from 'start'"""
        for i in range(start, start+count):
            self._data[i].self_del()
        del self._data[start:start+count]


class EntryListManager(list[EntryList]):
    """List of Lists of Entries.
    :todo: del
    """

    def __init__(self):
        super().__init__()

    @property
    def size(self):
        return len(self)

    def itemAdd(self, name: str, path: str):
        """Add new EntryList
        :param name: Associated name of EntryList
        :param path: Path to added EntryList
        :todo: return something
        """
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def itemUpdate(self, i: int, name: str, path: str):
        # old_entry = self[i]
        self[i].update(name, path)

    def itemDel(self, i: int) -> bool:
        if 0 <= i < self.size:
            del self[i]
            return True
        return False

    def print(self):
        for n, el in self:
            el.print()

    def findByName(self, s: str, i: int) -> bool:
        """Find existent CL by name [excluding i-th entry]
        :return: True if found
        """
        for j, el in enumerate(self):
            if el.name == s and j != i:
                return True
        return False

    def findByPath(self, s: str, i: int) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        for j, el in enumerate(self):
            if el.path == s and j != i:
                return True
        return False
