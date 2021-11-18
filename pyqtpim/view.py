"""Main GUI"""

from PySide2 import QtWidgets, QtGui
from contact import ContactsWidget
from todo import TodosWidget


class MainWindow(QtWidgets.QMainWindow):
    contacts: ContactsWidget
    todo: TodosWidget
    # misc
    tabs: QtWidgets.QTabWidget
    # actions
    actExit: QtWidgets.QAction
    actAbout: QtWidgets.QAction
    actEntryListAdd: QtWidgets.QAction
    actEntryListEdit: QtWidgets.QAction
    actEntryListDel: QtWidgets.QAction
    actEntryListInfo: QtWidgets.QAction

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
        self.tabs = QtWidgets.QTabWidget()
        self.contacts = ContactsWidget()
        self.todo = TodosWidget()
        self.tabs.addTab(self.contacts, "Contacts")
        self.tabs.addTab(self.todo, "ToDo")
        # that's all
        self.setCentralWidget(self.tabs)
        # attributes

    def createActions(self):
        # noinspection PyArgumentList
        self.actExit = QtWidgets.QAction(QtGui.QIcon(':/icons/power-standby.svg'),
                                         "E&xit", self,
                                         shortcut="Ctrl+Q",
                                         statusTip="Exit the application",
                                         triggered=self.close)
        # noinspection PyArgumentList
        self.actAbout = QtWidgets.QAction(QtGui.QIcon(':/icons/question-mark.svg'),
                                          "&About", self,
                                          statusTip="Show the application's About box",
                                          triggered=self.about)
        # noinspection PyArgumentList
        self.actEntryListAdd = QtWidgets.QAction(QtGui.QIcon(':/icons/plus.svg'),
                                                 "&New List", self,
                                                 shortcut="Ctrl+N",
                                                 statusTip="Add new List",
                                                 triggered=self.listAdd)
        # noinspection PyArgumentList
        self.actEntryListEdit = QtWidgets.QAction(QtGui.QIcon(':/icons/pencil.svg'),
                                                  "&Edit List", self,
                                                  shortcut="Ctrl+E",
                                                  statusTip="Edit current List",
                                                  triggered=self.listEdit)
        # noinspection PyArgumentList
        self.actEntryListDel = QtWidgets.QAction(QtGui.QIcon(':/icons/trash.svg'),
                                                 "&Del List", self,
                                                 shortcut="Ctrl+D",
                                                 statusTip="Delete current List",
                                                 triggered=self.listDel)
        # noinspection PyArgumentList
        self.actEntryListInfo = QtWidgets.QAction(QtGui.QIcon(':/icons/info.svg'),
                                                  "List &Info", self,
                                                  shortcut="Ctrl+I",
                                                  statusTip="Info about current List",
                                                  triggered=self.listInfo)

    def createMenus(self):
        menu_file = self.menuBar().addMenu("&File")
        menu_file.addAction(self.actExit)
        menu_edit = self.menuBar().addMenu("&Edit")
        menu_edit.addAction(self.actEntryListAdd)
        menu_edit.addAction(self.actEntryListEdit)
        menu_edit.addAction(self.actEntryListDel)
        menu_edit.addAction(self.actEntryListInfo)
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
        QtWidgets.QMessageBox.about(self, "About PyQtPIM", "PySide2 powered Personal Information Manager.")

    def listAdd(self):
        (self.contacts.sources.itemAdd, self.todo.sources.itemAdd)[self.tabs.currentIndex()]()

    def listEdit(self):
        (self.contacts.sources.itemEdit, self.todo.sources.itemEdit)[self.tabs.currentIndex()]()

    def listDel(self):
        (self.contacts.sources.itemDel, self.todo.sources.itemDel)[self.tabs.currentIndex()]()

    def listInfo(self):
        (self.contacts.sources.itemInfo, self.todo.sources.itemInfo)[self.tabs.currentIndex()]()
