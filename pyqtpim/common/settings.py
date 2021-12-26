# from __future__ import annotations
from typing import Any

from PySide2.QtCore import QCoreApplication, QSettings
from .data import Store, StoreList
from .enums import SetGroup


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
        """Get setting for group"""
        retvalue = None
        if key in {'col2show', 'colorder'}:
            s = MySettings.__settings
            s.beginGroup(group.value)
            if key == 'col2show':
                retvalue = s.value('col2show', list(range(12)))  # len(ColHeader)
            elif key == 'colorder':
                retvalue = s.value('colorder', list(range(13)))
            s.endGroup()
            retvalue = tuple(map(int, retvalue))
        return retvalue

    @staticmethod
    def set(group: SetGroup, key: str, val: Any):
        """Get setting for group"""
        if key in {'col2show', 'colorder'}:
            # print("Save", key, type(val), val)
            s = MySettings.__settings
            s.beginGroup(group.value)
            s.setValue(key, list(val))
            s.endGroup()

    @staticmethod
    def store_load(s_list: StoreList):
        s = MySettings.__settings
        s.beginGroup(s_list.setgroup_name())
        size = s.beginReadArray('store')
        for i in range(size):
            s.setArrayIndex(i)
            name = s.value('name')
            path = s.value('path')
            active = s.value('active')
            s_list.store_add(name, path, active)
        s.endArray()
        s.endGroup()

    @staticmethod
    def store_add(s_list: StoreList, store: Store):
        """Append Store array"""
        s = MySettings.__settings
        s.beginGroup(s_list.setgroup_name())
        s.beginWriteArray('store')
        s.setArrayIndex(s_list.size())
        s.setValue('name', store.name)
        s.setValue('path', store.dpath)
        s.setValue('active', store.active)
        s.endArray()
        s.endGroup()

    @staticmethod
    def store_upd(s_list: StoreList, i: int, store: Store):
        """:todo: check i on out of range"""
        s = MySettings.__settings
        s.beginGroup(s_list.setgroup_name())
        s.beginWriteArray('store')
        s.setArrayIndex(i)
        s.setValue('name', store.name)
        s.setValue('path', store.dpath)
        s.setValue('active', store.active)
        s.setArrayIndex(s_list.size() - 1)
        s.endArray()
        s.endGroup()

    @staticmethod
    def store_del(s_list: StoreList, i: int):
        s = MySettings.__settings
        s.beginGroup(s_list.setgroup_name())
        s.beginWriteArray('store')
        while i < s_list.size():
            store = s_list.store(i)
            s.setArrayIndex(i)
            s.setValue('name', store.name)
            s.setValue('path', store.dpath)
            s.setValue('active', store.active)
            i += 1
        s.setArrayIndex(i)
        s.remove("")
        s.endArray()
        s.setValue('list' + '/size', i)  # hack, but...
        s.endGroup()
