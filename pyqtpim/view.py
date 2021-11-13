"""Main GUI"""

from PySide2 import QtCore, QtGui, QtWidgets


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
        self.tab_contacts = QtWidgets.QWidget()
        self.contact_sources = QtWidgets.QListView(self.tab_contacts)
        self.contact_list = QtWidgets.QTableView(self.tab_contacts)
        self.contact_detail = QtWidgets.QWidget(self.tab_contacts)
        self.contact_detail.setMinimumSize(QtCore.QSize(128, 100))
        self.label_contact_fn = QtWidgets.QLabel(self.contact_detail)
        self.contact_fn = QtWidgets.QLineEdit(self.contact_detail)
        self.contact_family = QtWidgets.QLineEdit(self.contact_detail)
        self.contact_given = QtWidgets.QLineEdit(self.contact_detail)
        self.contact_email = QtWidgets.QLineEdit(self.contact_detail)
        self.contact_tel = QtWidgets.QLineEdit(self.contact_detail)
        # layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_contacts)
        self.horizontalLayout.addWidget(self.contact_sources)
        self.horizontalLayout.addWidget(self.contact_list)
        self.horizontalLayout.addWidget(self.contact_detail)

        self.tabWidget.addTab(self.tab_contacts, "Contacts")
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

        self.setCentralWidget(self.tabWidget)
        # attributes
        self.contact_fn.setReadOnly(True)
        self.contact_family.setReadOnly(True)
        self.contact_given.setReadOnly(True)
        self.contact_email.setReadOnly(True)
        self.contact_tel.setReadOnly(True)

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
