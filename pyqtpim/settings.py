from PySide2.QtCore import QCoreApplication, QSettings
from contact.collection import ABs

settings: QSettings


def setup_settings():
    def __w(s: QSettings):
        s.beginGroup("contacts")
        s.beginWriteArray("sources")
        for i, v in enumerate(ABs):
            s.setArrayIndex(i)
            s.setValue("name", v[0])
            s.setValue("path", v[1])
        s.endArray()
        s.endGroup()

    def __r(s):
        s.beginGroup("contacts")
        size = s.beginReadArray("sources")
        for i in range(size):
            s.setArrayIndex(i)
            name = s.value("name")
            path = s.value("path")
            ABs.append((name, path))
        s.endArray()
        s.endGroup()

    global settings
    QCoreApplication.setOrganizationName("TI_Eugene")
    QCoreApplication.setOrganizationDomain("eap.su")
    QCoreApplication.setApplicationName("PyQtPIM")
    QSettings.setDefaultFormat(QSettings.IniFormat)
    settings = QSettings()  # TODO: try QSettings.IniFormat
    __r(settings)
