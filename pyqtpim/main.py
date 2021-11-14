import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QCoreApplication
# 3. local
from settings import setup_settings
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
