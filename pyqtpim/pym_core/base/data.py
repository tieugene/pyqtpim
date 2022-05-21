"""Common vCard/iCal parents"""

# 1. std
# from __future__ import annotations
import inspect
import os
from _collections import OrderedDict
from enum import IntEnum, auto
from typing import Optional
# 2. 3rd
import vobject
# 3. local
from pym_core import exc


class EVObjType(IntEnum):
    VTodo = auto()


class VObj(object):
    """In-memory vobject object"""
    _data: vobject.base.Component   # loaded vobject
    # _type: EVObjType

    def __init__(self, data: vobject.base.Component):
        super().__init__()
        self._data = data

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

    def __repr__(self) -> str:
        return f"{self.__name} => {self.__dpath}"

    @property
    def name(self):
        return self.__name

    @property
    def dpath(self):
        return self.__dpath

    @property
    def active(self):
        return self.__active

    def as_dict(self):
        return {'name': self.name, 'path': self.dpath, 'active': self.active}

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

    def _load_one(self, entries, vobj_src: vobject.base.Component, fname: str):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")

    def load(self, entries):
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
                            self._load_one(entries, vobj_src, entry.name)
                        else:
                            raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")


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

    @property
    def store(self):
        return self._store

    @property
    def vobj(self):
        return self._vobj

    @property
    def full_path(self):
        return os.path.join(self._store.dpath, self._fname)

    def save(self) -> bool:
        """Save vobj back to disk"""
        with open(self.full_path, 'wt') as o_f:  # TODO: handle exceptions
            body = self._vobj.serialize()
            o_f.write(body)  # -> None
            return True

    def self_del(self) -> bool:
        os.remove(self.full_path)  # TODO: handle exceptions
        del self._vobj
        return True


# static class
class EntryList(object):
    """List of Entries, common for all Stores"""
    _list: list[Entry]
    __ready: bool

    def __init__(self):
        super().__init__()
        self._list = []
        self.__ready = False

    def size(self) -> int:
        return len(self._list)

    def entry_get(self, i: int) -> Optional[Entry]:
        """Get list item"""
        if 0 <= i < self.size():
            return self._list[i]

    def entry_add(self, entry: Entry) -> bool:
        self._list.append(entry)
        return True

    def entry_del(self, i: int):
        if 0 <= i < self.size():
            self._list[i].self_del()
            del self._list[i]
            return True
        return False


class StoreList(object):
    _item_cls: type  # successor-defined Store successor
    _entries: EntryList
    _list: list[Store]

    def __init__(self, entries: EntryList):
        super().__init__()
        self._entries = entries
        self._list = []

    def size(self) -> int:
        return len(self._list)

    def from_list(self, data: list[dict]):
        """:todo: error code"""
        for store in data:
            self.store_add(self._item_cls(store['name'], store['path'], store['active']))

    def to_list(self) -> list:
        """:todo: error code"""
        return [store.as_dict() for store in self._list]

    def store_get(self, i: int) -> Optional[Store]:
        if i < self.size():
            return self._list[i]

    def store_add(self, store: Store):
        """:todo: return something? e.g. index"""
        self._list.append(store)

    def store_del(self, i: int) -> bool:
        if 0 <= i < self.size():
            del self._list[i]
            return True
        return False

    def store_find(self, store: Store) -> int:
        return self._list.index(store)  # TODO: handle exception

    def store_findByName(self, name: str, i: int) -> bool:
        """Find existent CL by name excluding i-th entry
        :return: True if found
        """
        for j, store in enumerate(self._list):
            if store.name == name and j != i:
                return True
        return False

    def store_findByPath(self, dpath: str, i: int) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        for j, store in enumerate(self._list):
            if store.dpath == dpath and j != i:
                return True
        return False

    def load_entries(self):
        """Load entries from Stores paths"""
        for store in self._list:
            store.load(self._entries)
