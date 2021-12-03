"""Main GUI"""

from PySide2 import QtWidgets, QtGui
from contact import ContactsWidget
from todo import TodosWidget


class MainWindow(QtWidgets.QMainWindow):
    todo: TodosWidget
    contacts: ContactsWidget
    # misc
    tabs: QtWidgets.QTabWidget
    # actions
    actExit: QtWidgets.QAction
    actAbout: QtWidgets.QAction
    actEntryListAdd: QtWidgets.QAction
    actEntryListEdit: QtWidgets.QAction
    actEntryListDel: QtWidgets.QAction
    actEntryListInfo: QtWidgets.QAction
    actEntryCat: QtWidgets.QAction
    actEntryInside: QtWidgets.QAction
    actEntryAdd: QtWidgets.QAction
    actEntryEdit: QtWidgets.QAction
    actEntryDel: QtWidgets.QAction

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
        self.todo = TodosWidget()
        self.tabs.addTab(self.todo, "ToDo")
        self.contacts = ContactsWidget()
        self.tabs.addTab(self.contacts, "Contacts")
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
                                                 statusTip="Add new List",
                                                 triggered=self.listAdd)
        # noinspection PyArgumentList
        self.actEntryListEdit = QtWidgets.QAction(QtGui.QIcon(':/icons/pencil.svg'),
                                                  "&Edit List", self,
                                                  statusTip="Edit current List",
                                                  triggered=self.listEdit)
        # noinspection PyArgumentList
        self.actEntryListDel = QtWidgets.QAction(QtGui.QIcon(':/icons/trash.svg'),
                                                 "&Del List", self,
                                                 statusTip="Delete current List",
                                                 triggered=self.listDel)
        # noinspection PyArgumentList
        self.actEntryListInfo = QtWidgets.QAction(QtGui.QIcon(':/icons/info.svg'),
                                                  "List &Info", self,
                                                  shortcut="Ctrl+I",
                                                  statusTip="Info about current List",
                                                  triggered=self.listInfo)
        # noinspection PyArgumentList
        self.actEntryCat = QtWidgets.QAction(QtGui.QIcon(':/icons/eye.svg'),
                                             "Entry &File", self,
                                             shortcut="Ctrl+F",
                                             statusTip="Entry file content",
                                             triggered=self.entryCat)
        # noinspection PyArgumentList
        self.actEntryInside = QtWidgets.QAction(QtGui.QIcon(':/icons/code.svg'),
                                                "Entry &View", self,
                                                shortcut="Ctrl+V",
                                                statusTip="Entry inner structure",
                                                triggered=self.entryInside)
        # noinspection PyArgumentList
        self.actEntryAdd = QtWidgets.QAction(QtGui.QIcon(':/icons/plus.svg'),
                                             "&New Entry", self,
                                             shortcut="Ctrl+N",
                                             statusTip="Add new Entry",
                                             triggered=self.entryAdd)
        # noinspection PyArgumentList
        self.actEntryEdit = QtWidgets.QAction(QtGui.QIcon(':/icons/pencil.svg'),
                                              "&Edit Entry", self,
                                              shortcut="Ctrl+E",
                                              statusTip="Edit current Entry",
                                              triggered=self.entryEdit)
        # noinspection PyArgumentList
        self.actEntryDel = QtWidgets.QAction(QtGui.QIcon(':/icons/trash.svg'),
                                             "&Del Entry", self,
                                             shortcut="Ctrl+D",
                                             statusTip="Delete current Entry",
                                             triggered=self.entryDel)

    def createMenus(self):
        menu_file = self.menuBar().addMenu("&File")
        menu_file.addAction(self.actExit)
        menu_edit = self.menuBar().addMenu("&Edit")
        menu_edit.addAction(self.actEntryListAdd)
        menu_edit.addAction(self.actEntryListEdit)
        menu_edit.addAction(self.actEntryListDel)
        menu_edit.addSeparator()
        menu_edit.addAction(self.actEntryAdd)
        menu_edit.addAction(self.actEntryEdit)
        menu_edit.addAction(self.actEntryDel)
        menu_view = self.menuBar().addMenu("&View")
        menu_view.addAction(self.actEntryListInfo)
        menu_view.addSeparator()
        menu_view.addAction(self.actEntryCat)
        menu_view.addAction(self.actEntryInside)
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
        (self.todo.sources.itemAdd, self.contacts.sources.itemAdd)[self.tabs.currentIndex()]()

    def listEdit(self):
        (self.todo.sources.itemEdit, self.contacts.sources.itemEdit)[self.tabs.currentIndex()]()

    def listDel(self):
        (self.todo.sources.itemDel, self.contacts.sources.itemDel)[self.tabs.currentIndex()]()

    def listInfo(self):
        (self.todo.sources.itemInfo, self.contacts.sources.itemInfo)[self.tabs.currentIndex()]()

    def entryCat(self):
        """Show file content"""
        (self.todo.list.itemCat, self.contacts.list.itemCat)[self.tabs.currentIndex()]()

    def entryInside(self):
        """Show entry structure"""
        self.todo.list.itemInside()

    def entryAdd(self):
        self.todo.list.itemAdd()

    def entryEdit(self):
        self.todo.list.itemEdit()

    def entryDel(self):
        self.todo.list.itemDel()
