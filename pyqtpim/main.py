import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QFile, QCoreApplication
from PySide2.QtUiTools import QUiLoader
# 3. local
from settings import handle_settings
from contact.model import ContactListModel, ContactListManagerModel
from contact.collection import ABs, ContactList, ContactListManager

mw = None


def load_ui():
    loader = QUiLoader()
    path = os.fspath(Path(__file__).resolve().parent / "mainwindow.ui")
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    retvalue = loader.load(ui_file)
    ui_file.close()
    return retvalue


def refresh_contact_details(idx):
    data = idx.model().getBack(idx)
    mw.contact_fn.setText(data.getFN())
    mw.contact_family.setText(data.getFamily())
    mw.contact_given.setText(data.getGiven())
    mw.contact_email.setText(data.getEmail())
    mw.contact_tel.setText(data.getTel())


def main():
    global mw
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    handle_settings()
    app = QApplication(sys.argv)
    mw = load_ui()
    # prepare data
    clm = ContactListManager()
    for n, p in ABs:
        # - AB list
        cl = ContactList(p)
        cl.load()
        cl_model = ContactListModel(cl=cl)
        mw.contact_list.setModel(cl_model)
        clm.add(n, cl)
    clm_model = ContactListManagerModel(mgr=clm)
    mw.contact_sources.setModel(clm_model)
    # connect
    mw.contact_list.activated.connect(refresh_contact_details)
    # go
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
