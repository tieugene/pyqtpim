from PySide2.QtCore import QCoreApplication, QSettings


class MySettings:
    """QSettings extender"""
    __settings: QSettings
    AB: list[(str, str)] = []

    @staticmethod
    def setup():
        QCoreApplication.setOrganizationName("TI_Eugene")
        QCoreApplication.setOrganizationDomain("eap.su")
        QCoreApplication.setApplicationName("PyQtPIM")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        MySettings.__settings = QSettings()
        MySettings.__list_preload('contacts')

    @staticmethod
    def __list_preload(group: str):
        s = MySettings.__settings
        s.beginGroup(group)
        size = s.beginReadArray('list')
        for i in range(size):
            s.setArrayIndex(i)
            name = s.value('name')
            path = s.value('path')
            MySettings.AB.append((name, path))
        s.endArray()
        s.endGroup()

    @staticmethod
    def list_append(group: str, data: dict):
        """Append array in group"""
        s = MySettings.__settings
        s.beginGroup(group)
        s.beginWriteArray('list')
        s.setArrayIndex(len(MySettings.AB))
        for k, v in data.items():
            s.setValue(k, v)
        s.endArray()
        s.endGroup()
        MySettings.AB.append((data['name'], data['path']))

    @staticmethod
    def list_update(group: str, i: int, data: dict):
        s = MySettings.__settings
        s.beginGroup(group)
        s.beginWriteArray('list')
        s.setArrayIndex(i)
        for k, v in data.items():
            s.setValue(k, v)
        s.setArrayIndex(len(MySettings.AB) - 1)
        s.endArray()
        s.endGroup()
        MySettings.AB[i] = (data['name'], data['path'])

    @staticmethod
    def list_del(group: str, i: int):
        del MySettings.AB[i]
        s = MySettings.__settings
        s.beginGroup(group)
        s.beginWriteArray('list')
        while i < len(MySettings.AB):
            s.setArrayIndex(i)
            s.setValue('name', MySettings.AB[i][0])
            s.setValue('path', MySettings.AB[i][1])
            i += 1
        s.setArrayIndex(i)
        s.remove("")
        s.endArray()
        s.setValue('list' + '/size', i)  # hack, but...
        s.endGroup()
