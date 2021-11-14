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


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    setup_settings()
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
