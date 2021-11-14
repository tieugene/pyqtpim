"""Main GUI"""

from PySide2 import QtWidgets
from contact.view import ContactsWidget


class MainWindow(QtWidgets.QMainWindow):
    contacts: ContactsWidget

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
        self.actExit = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                                         statusTip="Exit the application", triggered=self.close)
        self.actAbout = QtWidgets.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)
        self.actAddContactSource = QtWidgets.QAction("&Add Contact Source", self,
                                                     statusTip="Add contact source",
                                                     triggered=self.contacts.sources.addEntry)
        self.actEditContactSource = QtWidgets.QAction("&Edit Contact Source", self,
                                                      statusTip="Edit current contact source",
                                                      triggered=self.contacts.sources.editEntry)
        self.actDelContactSource = QtWidgets.QAction("&Del Contact Source", self,
                                                     statusTip="Delete current contact source",
                                                     triggered=self.contacts.sources.delEntry)

    def createMenus(self):
        self.menuFile = self.menuBar().addMenu("&File")
        self.menuFile.addAction(self.actExit)
        self.menuEdit = self.menuBar().addMenu("&Edit")
        self.menuEdit.addAction(self.actAddContactSource)
        self.menuEdit.addAction(self.actEditContactSource)
        self.menuEdit.addAction(self.actDelContactSource)
        self.menuView = self.menuBar().addMenu("&View")
        self.menuHelp = self.menuBar().addMenu("&Help")
        self.menuHelp.addAction(self.actAbout)

    def createToolBars(self):
        self.toolbarFile = self.addToolBar("File")
        self.toolbarEdit = self.addToolBar("Edit")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    # actions
    def about(self):
        QtWidgets.QMessageBox.about(self, "About PyQtPIM",
                "Python & Qt powered Personal Information Manager\n(Contacs, ToDos, Calendar, Events, Journal).")
