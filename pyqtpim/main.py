import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QCoreApplication
# 3. local
from common import MySettings
from view import MainWindow
from todo import store_list
from pyqtpim_rc import qInitResources


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    qInitResources()
    MySettings.setup()
    MySettings.store_load(store_list)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
