from PySide2.QtCore import QCoreApplication, QSettings


class MySettings:
    """QSettings extender"""
    settings: QSettings
    AB: list[(str, str)] = []

    @staticmethod
    def setup():
        def __ab_preload(s):
            s.beginGroup('contacts')
            size = s.beginReadArray('sources')
            for i in range(size):
                s.setArrayIndex(i)
                name = s.value('name')
                path = s.value('path')
                MySettings.AB.append((name, path))
            s.endArray()
            s.endGroup()
        QCoreApplication.setOrganizationName("TI_Eugene")
        QCoreApplication.setOrganizationDomain("eap.su")
        QCoreApplication.setApplicationName("PyQtPIM")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        MySettings.settings = QSettings()
        __ab_preload(MySettings.settings)

    @staticmethod
    def ab_append(data: dict):
        """Append array in group"""
        s = MySettings.settings
        s.beginGroup('contacts')
        s.beginWriteArray('sources')
        s.setArrayIndex(len(MySettings.AB))
        for k, v in data.items():
            s.setValue(k, v)
        s.endArray()
        s.endGroup()
        MySettings.AB.append((data['name'], data['path']))

    @staticmethod
    def ab_update(i: int, data: dict):
        s = MySettings.settings
        s.beginGroup('contacts')
        s.beginWriteArray('sources')
        s.setArrayIndex(i)
        for k, v in data.items():
            s.setValue(k, v)
        s.setArrayIndex(len(MySettings.AB) - 1)
        s.endArray()
        s.endGroup()
        MySettings.AB[i] = (data['name'], data['path'])

    @staticmethod
    def ab_del(i: int):
        del MySettings.AB[i]
        s = MySettings.settings
        s.beginGroup('contacts')
        s.beginWriteArray('sources')
        while i < len(MySettings.AB):
            s.setArrayIndex(i)
            s.setValue('name', MySettings.AB[i][0])
            s.setValue('path', MySettings.AB[i][1])
            i += 1
        s.setArrayIndex(i)
        s.remove("")
        s.endArray()
        s.setValue('sources' + '/size', i)  # hack, but...
        s.endGroup()
