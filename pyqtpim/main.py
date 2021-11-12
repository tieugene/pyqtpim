import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QFile, QCoreApplication, QSettings
from PySide2.QtUiTools import QUiLoader
# 3. local
from contact.model import ContactListModel, ContactListManagerModel
from contact.collection import ContactList, ContactListManager

test_ABs = []  # [('AB', '/Volumes/Trash/Documents/AB'),]


def handle_settings():
    def __w(s: QSettings):
        s.beginGroup("contacts")
        s.beginWriteArray("sources")
        for i, v in enumerate(test_ABs):
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
            test_ABs.append((name, path))
        s.endArray()
        s.endGroup()

    QCoreApplication.setOrganizationName("TI_Eugene")
    QCoreApplication.setOrganizationDomain("eap.su")
    QCoreApplication.setApplicationName("PyQtPIM")
    QSettings.setDefaultFormat(QSettings.IniFormat)
    settings = QSettings()  # TODO: try QSettings.IniFormat
    __r(settings)


def load_ui():
    loader = QUiLoader()
    path = os.fspath(Path(__file__).resolve().parent / "mainwindow.ui")
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    retvalue = loader.load(ui_file)
    ui_file.close()
    return retvalue


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    handle_settings()
    app = QApplication(sys.argv)
    mw = load_ui()
    # prepare data
    clm = ContactListManager()
    for n, p in test_ABs:
        # - AB list
        cl = ContactList(p)
        cl.load()
        cl_model = ContactListModel(cl=cl)
        mw.contact_list.setModel(cl_model)
        clm.add(n, cl)
    clm_model = ContactListManagerModel(mgr=clm)
    mw.contact_sources.setModel(clm_model)
    # go
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
