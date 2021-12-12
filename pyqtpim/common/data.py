"""Common vCard/iCal parents"""

# 1. std
import inspect
from _collections import OrderedDict
from enum import IntEnum
from typing import Any, Optional
# 2. 3rd
import vobject
# 3. local


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


class EntryList:
    """FIXME: stub"""


class EntryListManager:
    """FIXME: stub"""
