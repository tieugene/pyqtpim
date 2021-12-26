"""Common vCard/iCal parents"""

# 1. std
# from __future__ import annotations
import inspect
import os
from _collections import OrderedDict
from enum import IntEnum, auto
from typing import Any, Optional
# 2. 3rd
import vobject
# 3. local
from . import exc, enums


class EVObjType(IntEnum):
    VTodo = auto()


class VObj(object):
    """In-memory vobject object"""
    _data: vobject.base.Component   # loaded vobject
    # _type: EVObjType
    _name2func: dict[IntEnum, Any]  # mapping model column name to getter

    def __init__(self, data: vobject.base.Component):
        super().__init__()
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


class Store(object):
    """:todo: unload (before deletion)"""
    __name: str     # displayed name (uniq)
    __dpath: str    # directory path (uniq)
    __active: bool  # show/hide in StoreListView
    __ready: bool   # ? loaded from source
    __type: EVObjType

    def __init__(self, name: str, dpath: str, active: bool):
        super().__init__()
        self.__name = name
        self.__dpath = dpath
        self.__active = active
        # self.__ready = False

    @property
    def name(self):
        return self.__name

    @property
    def dpath(self):
        return self.__dpath

    @property
    def active(self):
        return self.__active

    @name.setter
    def name(self, name: str):
        self.__name = name

    @dpath.setter
    def dpath(self, dpath: str):
        if dpath != self.__dpath:
            self.__dpath = dpath
            self.__active = False
            # TODO: reload entries in EntryList

    @active.setter
    def active(self, active: bool):
        self.__active = active
        # TODO: refresh filter

    def _load_one(self, vobj_src: vobject.base.Component, fname: str):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def __load(self):
        """Load entries from dir"""
        if self.__dpath:
            # print(f"{self.__name}: Loading from {self.__path}")
            with os.scandir(self.__dpath) as itr:
                for entry in itr:
                    if not entry.is_file():
                        continue
                    with open(entry.path, 'rt') as stream:
                        # TODO: chk mimetype
                        if vobj_src := vobject.readOne(stream):
                            self._load_one(vobj_src, entry.name)
                        else:
                            raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")


# static class
class StoreList(object):
    _set_group: enums.SetGroup
    _data: list[Store]

    def __init__(self):
        super().__init__()
        self._data = []
        self._set_group = enums.SetGroup.ToDo  # FIXME: dirty

    def size(self) -> int:
        return len(self._data)

    def setgroup_name(self) -> str:
        return self._set_group.value

    def store(self, i: int) -> Store:
        if i < self.size():
            return self._data[i]

    def store_add(self, name: str, path: str, active: bool):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def store_del(self, i: int) -> bool:
        if 0 <= i < self.size():
            del self._data[i]
            return True
        return False

    def store_findByName(self, name: str, i: int) -> bool:
        """Find existent CL by name excluding i-th entry
        :return: True if found
        """
        for j, store in enumerate(self._data):
            if store.name == name and j != i:
                return True
        return False

    def store_findByPath(self, dpath: str, i: int) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        for j, store in enumerate(self._data):
            if store.dpath == dpath and j != i:
                return True
        return False


class Entry(object):
    """Interim to link VObj, its source and Source"""
    _vobj: VObj
    _store: Store
    _fname: str  # file name

    def __init__(self, vobj: VObj, store: Store, fname: str):
        super().__init__()
        self._vobj = vobj
        self._store = store
        self._fname = fname


# static class
class EntryList(object):
    """List of Entries, common for all Stores"""
    _data: list[Entry]
    __ready: bool

    def __init__(self):
        super().__init__()
        self._data = []
        self.__ready = False

    def size(self) -> int:
        return len(self._data)

    def entry_add(self, entry: Entry):
        self._data.append(entry)

    def entry_del(self, i: int):
        if i < self.size():
            del self._data[i]

    def entry(self, i: int) -> Entry:
        """Get list item"""
        if i < self.size():
            return self._data[i]
