import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QFile, QCoreApplication
from PySide2.QtUiTools import QUiLoader
# 3. local
from settings import setup_settings
from contact.model import ContactListModel, ContactListManagerModel
from contact.collection import ABs, ContactList, ContactListManager
from view import MainWindow

mw = None


def refresh_contact_details(idx):
    data = idx.model().getBack(idx)
    mw.contact_fn.setText(data.getFN())
    mw.contact_family.setText(data.getFamily())
    mw.contact_given.setText(data.getGiven())
    mw.contact_email.setText(data.getEmail())
    mw.contact_tel.setText(data.getTel())


def setup_ui():
    loader = QUiLoader()
    path = os.fspath(Path(__file__).resolve().parent / "mainwindow.ui")
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    retvalue = loader.load(ui_file)
    ui_file.close()
    return retvalue


def setup_models(w):
    clm = ContactListManager()
    for n, p in ABs:
        cl = ContactList(p)
        cl.load()
        cl_model = ContactListModel(cl=cl)
        w.contact_list.setModel(cl_model)
        clm.add(n, cl)
    clm_model = ContactListManagerModel(mgr=clm)
    w.contact_sources.setModel(clm_model)


def setup_ss(w):
    mw.contact_list.activated.connect(refresh_contact_details)


def main():
    global mw
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    setup_settings()
    app = QApplication(sys.argv)
    # mw = setup_ui()   # lite
    mw = MainWindow()
    setup_models(mw)
    setup_ss(mw)
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
