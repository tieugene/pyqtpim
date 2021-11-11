import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QFile, QCoreApplication
from PySide2.QtUiTools import QUiLoader
# 3. local
from contact.mgr import ContactListManager, ContactListModel
from contact.collection import ContactList

indir = '/Volumes/Trash/Documents/AB'


def load_ui():
    loader = QUiLoader()
    path = os.fspath(Path(__file__).resolve().parent / "mainwindow.ui")
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    retvalue = loader.load(ui_file)
    ui_file.close()
    return retvalue


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    mw = load_ui()
    cl_mgr = ContactListManager()
    cl_mgr.add(ContactList('AB', indir))
    cl_mgr.reload()
    cl_model = ContactListModel(mgr=cl_mgr)
    mw.contact_sources.setModel(cl_model)
    mw.show()
    sys.exit(app.exec_())
