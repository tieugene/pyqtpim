# from __future__ import annotations
import json
from typing import Any, Union, Optional

from PySide2.QtCore import QCoreApplication, QSettings
from .enums import SetGroup


class MySettings:
    """QSettings extender
    TODO: wrap 'set's into ','.join(set)
    """
    __settings: QSettings

    @staticmethod
    def valueToBool(value: Union[bool, str]) -> bool:
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    @staticmethod
    def setup():
        QCoreApplication.setOrganizationName("TI_Eugene")
        QCoreApplication.setOrganizationDomain("eap.su")
        QCoreApplication.setApplicationName("PyQtPIM")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        MySettings.__settings = QSettings()

    @staticmethod
    def get(group: SetGroup, key: str) -> Optional[list]:
        """Get setting for group"""
        retvalue = None
        if key in {'col2show', 'colorder', 'store'}:
            s = MySettings.__settings
            s.beginGroup(group.value)
            if key == 'col2show':
                retvalue = tuple(map(int, s.value('col2show', list(range(12)))))  # len(ColHeader)
            elif key == 'colorder':
                retvalue = tuple(map(int, s.value('colorder', list(range(12)))))
            elif key == 'store':
                retvalue = json.loads(s.value('store', '[]'))
            s.endGroup()
            # retvalue = tuple(map(int, retvalue))
        return retvalue

    @staticmethod
    def set(group: SetGroup, key: str, val: Any):
        """Get setting for group"""
        if key in {'col2show', 'colorder', 'store'}:
            # print("Save", key, type(val), val)
            s = MySettings.__settings
            s.beginGroup(group.value)
            if key == 'store':
                to_save = json.dumps(val)
            else:
                to_save = list(val)
            s.setValue(key, to_save)
            s.endGroup()
