from enum import Enum
from typing import Any

from PySide2.QtCore import QCoreApplication, QSettings
# from todo import ColHeader


class SetGroup(Enum):
    Contacts = 'contacts'
    ToDo = 'todo'


class MySettings:
    """QSettings extender
    TODO: wrap 'set's into ','.join(set)
    """
    __settings: QSettings

    @staticmethod
    def setup():
        QCoreApplication.setOrganizationName("TI_Eugene")
        QCoreApplication.setOrganizationDomain("eap.su")
        QCoreApplication.setApplicationName("PyQtPIM")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        MySettings.__settings = QSettings()

    @staticmethod
    def get(group: SetGroup, key: str) -> Any:
        retvalue = None
        if key in {'col2show', 'colorder'}:
            s = MySettings.__settings
            s.beginGroup(group.value)
            if key == 'col2show':
                retvalue = s.value('col2show', set(range(12)))  # len(ColHeader)
            elif key == 'colorder':
                retvalue = s.value('colorder', range(13))
                retvalue = map(int, retvalue)
            s.endGroup()
        return retvalue

    @staticmethod
    def set(group: SetGroup, key: str, val: Any):
        if key in {'col2show', 'colorder'}:
            s = MySettings.__settings
            s.beginGroup(group.value)
            s.setValue(key, val)
            s.endGroup()
