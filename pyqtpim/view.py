"""Main GUI"""

from PySide2 import QtWidgets
from contact.view import ContactsWidget


class MainWindow(QtWidgets.QMainWindow):
    contacts: ContactsWidget

    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createActions()

    def createWidgets(self):
        # order
        tabs = QtWidgets.QTabWidget()
        self.contacts = ContactsWidget()
        tabs.addTab(self.contacts, "Contacts")
        tabs.addTab(QtWidgets.QWidget(), "ToDo")
        # that's all
        self.setCentralWidget(tabs)
        # attributes

    def createMenus(self):
        self.menuFile = self.menuBar().addMenu("&File")
        self.menuEdit = self.menuBar().addMenu("&Edit")
        self.menuView = self.menuBar().addMenu("&View")
        self.menuHelp = self.menuBar().addMenu("&Help")

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.editToolBar = self.addToolBar("Edit")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createActions(self):
        ...
