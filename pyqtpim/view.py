"""Main GUI"""

from PySide2 import QtCore, QtGui, QtWidgets
from contact.view import ContactsWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createActions()

    def createWidgets(self):
        # order
        self.tabWidget = QtWidgets.QTabWidget()
        self.contacts = ContactsWidget()
        self.tabWidget.addTab(self.contacts, "Contacts")
        # todo
        self.tab_tasks = QtWidgets.QWidget()
        self.tasks_to_show = QtWidgets.QListWidget(self.tab_tasks)
        QtWidgets.QListWidgetItem(self.tasks_to_show)
        QtWidgets.QListWidgetItem(self.tasks_to_show)
        QtWidgets.QListWidgetItem(self.tasks_to_show)
        QtWidgets.QListWidgetItem(self.tasks_to_show)
        QtWidgets.QListWidgetItem(self.tasks_to_show)
        self.tasks_sources = QtWidgets.QListView(self.tab_tasks)
        self.task_list = QtWidgets.QTableView(self.tab_tasks)
        self.task_detail = QtWidgets.QWidget(self.tab_tasks)
        self.tabWidget.addTab(self.tab_tasks, "ToDo")
        # that's all
        self.setCentralWidget(self.tabWidget)
        # attributes

        self.tasks_to_show.item(0).setText("Inbox")
        self.tasks_to_show.item(1).setText("All")
        self.tasks_to_show.item(2).setText("Today")
        self.tasks_to_show.item(3).setText("Tomorrow")
        self.tasks_to_show.item(4).setText("Week")

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
