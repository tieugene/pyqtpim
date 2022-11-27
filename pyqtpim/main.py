#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QCoreApplication
# 3. local
from common import MySettings
from todo import store_model
from view import MainWindow
from pyqtpim_rc import qInitResources


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
