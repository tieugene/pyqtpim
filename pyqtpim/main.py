import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QFile, QCoreApplication
from PySide2.QtUiTools import QUiLoader
# 3. local
from contact.model import ContactListModel, ContactListManagerModel
from contact.collection import ContactList, ContactListManager

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
    # prepare data
    # - AB list
    cl = ContactList(indir)
    cl.load()
    clm = ContactListManager()
    clm.add('AB', cl)
    # clm.reload()
    clm_model = ContactListManagerModel(mgr=clm)
    mw.contact_sources.setModel(clm_model)
    # - AB
    cl_model = ContactListModel(cl=cl)
    mw.contact_list.setModel(cl_model)
    # go
    mw.show()
    sys.exit(app.exec_())
