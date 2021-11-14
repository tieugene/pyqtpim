from PySide2.QtCore import QCoreApplication, QSettings


class MySettings:
    """QSettings extender"""
    settings: QSettings
    AB: list = []

    @staticmethod
    def setup():

        def __r(s):
            s.beginGroup("contacts")
            size = s.beginReadArray("sources")
            for i in range(size):
                s.setArrayIndex(i)
                name = s.value("name")
                path = s.value("path")
                MySettings.AB.append((name, path))
            s.endArray()
            s.endGroup()

        QCoreApplication.setOrganizationName("TI_Eugene")
        QCoreApplication.setOrganizationDomain("eap.su")
        QCoreApplication.setApplicationName("PyQtPIM")
        QSettings.setDefaultFormat(QSettings.IniFormat)
        MySettings.settings = QSettings()
        __r(MySettings.settings)
