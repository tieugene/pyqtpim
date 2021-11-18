from enum import Enum

from PySide2.QtCore import QCoreApplication, QSettings


class SetGroup(Enum):
    Contacts = 'contacts'
    ToDo = 'todo'


class MySettings:
    """QSettings extender"""
    __settings: QSettings
    __cache: dict[SetGroup]

    @staticmethod
    def setup():
        QCoreApplication.setOrganizationName("TI_Eugene")
        QCoreApplication.setOrganizationDomain("eap.su")
        QCoreApplication.setApplicationName("PyQtPIM")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        MySettings.__settings = QSettings()
        MySettings.__cache = {
            SetGroup.Contacts: [],
            SetGroup.ToDo: []
        }
        MySettings.__list_preload(SetGroup.Contacts)

    @staticmethod
    def __list_preload(group: SetGroup):
        s = MySettings.__settings
        s.beginGroup(group.value)
        size = s.beginReadArray('list')
        for i in range(size):
            s.setArrayIndex(i)
            name = s.value('name')
            path = s.value('path')
            MySettings.__cache[group].append((name, path))
        s.endArray()
        s.endGroup()

    @staticmethod
    def list_ls(group: SetGroup) -> list:
        return MySettings.__cache[group]

    @staticmethod
    def list_append(group: SetGroup, data: dict):
        """Append array in group"""
        s = MySettings.__settings
        s.beginGroup(group.value)
        s.beginWriteArray('list')
        s.setArrayIndex(len(MySettings.__cache[group]))
        for k, v in data.items():
            s.setValue(k, v)
        s.endArray()
        s.endGroup()
        MySettings.__cache[group].append((data['name'], data['path']))

    @staticmethod
    def list_update(group: SetGroup, i: int, data: dict):
        s = MySettings.__settings
        s.beginGroup(group.value)
        s.beginWriteArray('list')
        s.setArrayIndex(i)
        for k, v in data.items():
            s.setValue(k, v)
        s.setArrayIndex(len(MySettings.__cache[group]) - 1)
        s.endArray()
        s.endGroup()
        MySettings.__cache[group][i] = (data['name'], data['path'])

    @staticmethod
    def list_del(group: SetGroup, i: int):
        del MySettings.__cache[group][i]
        s = MySettings.__settings
        s.beginGroup(group.value)
        s.beginWriteArray('list')
        while i < len(MySettings.__cache[group]):
            s.setArrayIndex(i)
            s.setValue('name', MySettings.__cache[group][i][0])
            s.setValue('path', MySettings.__cache[group][i][1])
            i += 1
        s.setArrayIndex(i)
        s.remove("")
        s.endArray()
        s.setValue('list' + '/size', i)  # hack, but...
        s.endGroup()
