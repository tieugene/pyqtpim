#!/usr/bin/env python3
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QCoreApplication
# 3. local
from base import MySettings
from todo import store_model
from view import MainWindow
from pym_gui_rc import qInitResources


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    qInitResources()
    MySettings.setup()
    app = QApplication(sys.argv)
    mw = MainWindow()
    store_model.load_self()
    store_model.load_entries()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()