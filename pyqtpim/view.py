"""Main GUI"""

from PySide2 import QtWidgets
from contact.view import ContactsWidget


class MainWindow(QtWidgets.QMainWindow):
    contacts: ContactsWidget
    actExit: QtWidgets.QAction
    actAbout: QtWidgets.QAction
    actAddContactSource: QtWidgets.QAction
    actEditContactSource: QtWidgets.QAction
    actDelContactSource: QtWidgets.QAction

    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.setWindowTitle("PyQtPIM")

    def createWidgets(self):
        # order
        tabs = QtWidgets.QTabWidget()
        self.contacts = ContactsWidget()
        tabs.addTab(self.contacts, "Contacts")
        tabs.addTab(QtWidgets.QWidget(), "ToDo")
        # that's all
        self.setCentralWidget(tabs)
        # attributes

    def createActions(self):
        self.actExit = QtWidgets.QAction("E&xit", self,
                                         shortcut="Ctrl+Q",
                                         statusTip="Exit the application",
                                         triggered=self.close)
        self.actAbout = QtWidgets.QAction("&About", self,
                                          statusTip="Show the application's About box",
                                          triggered=self.about)
        self.actAddContactSource = QtWidgets.QAction("&Add Contact Source", self,
                                                     shortcut="Ctrl+N",
                                                     statusTip="Add contact source",
                                                     triggered=self.contacts.sources.itemAdd)
        self.actEditContactSource = QtWidgets.QAction("&Edit Contact Source", self,
                                                      shortcut="Ctrl+E",
                                                      statusTip="Edit current contact source",
                                                      triggered=self.contacts.sources.itemEdit)
        self.actDelContactSource = QtWidgets.QAction("&Del Contact Source", self,
                                                     shortcut="Ctrl+D",
                                                     statusTip="Delete current contact source",
                                                     triggered=self.contacts.sources.itemDel)

    def createMenus(self):
        menu_file = self.menuBar().addMenu("&File")
        menu_file.addAction(self.actExit)
        menu_edit = self.menuBar().addMenu("&Edit")
        menu_edit.addAction(self.actAddContactSource)
        menu_edit.addAction(self.actEditContactSource)
        menu_edit.addAction(self.actDelContactSource)
        # menuView = self.menuBar().addMenu("&View")
        menu_help = self.menuBar().addMenu("&Help")
        menu_help.addAction(self.actAbout)

    def createToolBars(self):
        self.addToolBar("File")
        self.addToolBar("Edit")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    # actions
    def about(self):
        QtWidgets.QMessageBox.about(self, "About PyQtPIM",
                                    "Python & Qt powered Personal Information Manager.")
