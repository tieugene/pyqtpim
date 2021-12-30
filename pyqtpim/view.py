"""Main GUI"""

from PySide2 import QtWidgets, QtGui
from contact import ContactsWidget
from todo import TodosWidget
from form import SettingsView


class MainWindow(QtWidgets.QMainWindow):
    todo: TodosWidget
    contacts: ContactsWidget
    # misc
    tabs: QtWidgets.QTabWidget
    settings_view: SettingsView
    # actions
    actExit: QtWidgets.QAction
    actAbout: QtWidgets.QAction
    actSettings: QtWidgets.QAction
    actStoreAdd: QtWidgets.QAction
    actStoreEdit: QtWidgets.QAction
    actStoreDel: QtWidgets.QAction
    actStoreInfo: QtWidgets.QAction
    actStoreReload: QtWidgets.QAction
    actStoreFakeSync: QtWidgets.QAction
    actStoreSync: QtWidgets.QAction
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
        self.settings_view = SettingsView()
        # actions handling
        self.updateActionsStore(False)
        self.updateActionsEntry(False)
        self.todo.stores.actionsChange.connect(self.updateActionsStore)
        self.todo.list.actionsChange.connect(self.updateActionsEntry)
        self.todo.list.model().counter.connect(self.updateStatus)

    def createWidgets(self):
        # order
        self.tabs = QtWidgets.QTabWidget()
        self.todo = TodosWidget()
        self.tabs.addTab(self.todo, "ToDo")
        # self.contacts = ContactsWidget()
        # self.tabs.addTab(self.contacts, "Contacts")
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
        self.actSettings = QtWidgets.QAction(QtGui.QIcon(':/icons/cog.svg'),
                                             "&Settings", self,
                                             statusTip="Define settings",
                                             triggered=self.settings)
        # noinspection PyArgumentList
        self.actStoreAdd = QtWidgets.QAction(QtGui.QIcon(':/icons/plus.svg'),
                                             "&New Store", self,
                                             statusTip="Add new Store",
                                             triggered=self.storeAdd)
        # noinspection PyArgumentList
        self.actStoreEdit = QtWidgets.QAction(QtGui.QIcon(':/icons/pencil.svg'),
                                              "&Edit Store", self,
                                              statusTip="Edit current Store",
                                              triggered=self.storeEdit)
        # noinspection PyArgumentList
        self.actStoreDel = QtWidgets.QAction(QtGui.QIcon(':/icons/trash.svg'),
                                             "&Del Store", self,
                                             statusTip="Delete current Store",
                                             triggered=self.storeDel)
        # noinspection PyArgumentList
        self.actStoreInfo = QtWidgets.QAction(QtGui.QIcon(':/icons/info.svg'),
                                              "Store &Info", self,
                                              shortcut="Ctrl+I",
                                              statusTip="Info about current Store",
                                              triggered=self.storeInfo)
        # noinspection PyArgumentList
        self.actStoreReload = QtWidgets.QAction(QtGui.QIcon(':/icons/cloud-download.svg'),
                                                "&Reload Store", self,
                                                shortcut="Ctrl+R",
                                                statusTip="Reload current Store",
                                                triggered=self.storeReload)
        # noinspection PyArgumentList
        self.actStoreFakeSync = QtWidgets.QAction(QtGui.QIcon(':/icons/transfer.svg'),
                                                  "&Sync Store (fake)", self,
                                                  shortcut="Ctrl+S",
                                                  statusTip="Sync current Store (dry run)",
                                                  triggered=self.storeFakeSync)
        # noinspection PyArgumentList
        self.actStoreSync = QtWidgets.QAction(QtGui.QIcon(':/icons/transfer.svg'),
                                              "Sync Store", self,
                                              statusTip="Sync current Store (real)",
                                              triggered=self.storeSync)
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
        menu_file.addAction(self.actSettings)
        menu_file.addAction(self.actExit)
        menu_store = self.menuBar().addMenu("&Store")
        menu_store.addAction(self.actStoreAdd)
        menu_store.addAction(self.actStoreEdit)
        menu_store.addAction(self.actStoreDel)
        menu_store.addSeparator()
        menu_store.addAction(self.actStoreInfo)
        menu_store.addAction(self.actStoreReload)
        menu_entry = self.menuBar().addMenu("&Entry")
        menu_entry.addAction(self.actEntryAdd)
        menu_entry.addAction(self.actEntryEdit)
        menu_entry.addAction(self.actEntryDel)
        menu_entry.addSeparator()
        menu_entry.addAction(self.actEntryCat)
        menu_entry.addAction(self.actEntryInside)
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

    def settings(self):
        self.settings_view.load()
        if self.settings_view.exec_():
            self.todo.list.loadCol2Show()

    def storeAdd(self):
        # (self.todo.stores.storeAdd, self.contacts.sources.storeAdd)[self.tabs.currentIndex()]()
        self.todo.stores.storeAdd()

    def storeEdit(self):
        self.todo.stores.storeEdit()

    def storeDel(self):
        self.todo.stores.storeDel()

    def storeInfo(self):
        self.todo.stores.storeInfo()

    def storeReload(self):
        self.todo.stores.stores_reload()

    def storeFakeSync(self):
        ...

    def storeSync(self):
        ...

    def entryCat(self):
        """Show file content"""
        self.todo.list.entryCat()

    def entryInside(self):
        """Show entry structure"""
        self.todo.list.entryInside()

    def entryAdd(self):
        self.todo.list.entryAdd()

    def entryEdit(self):
        self.todo.list.entryEdit()

    def entryDel(self):
        self.todo.list.entryDel()

    def updateActionsStore(self, state: bool):
        self.actStoreEdit.setEnabled(state)
        self.actStoreDel.setEnabled(state)
        self.actStoreInfo.setEnabled(state)

    def updateActionsEntry(self, state: bool):
        self.actEntryEdit.setEnabled(state)
        self.actEntryDel.setEnabled(state)
        self.actEntryCat.setEnabled(state)
        self.actEntryInside.setEnabled(state)

    def updateStatus(self, v: int):
        self.statusBar().showMessage(f"Count: {v}")
