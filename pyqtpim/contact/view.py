"""GUI representation of Contact things"""

from PySide2 import QtCore, QtWidgets


class ContactSources(QtWidgets.QListView):
    def __init__(self, parent):
        super().__init__(parent)


class ContactList(QtWidgets.QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        # self.setEditTriggers(self.NoEditTriggers)
        # self.setSortingEnabled(True) # requires sorting itself
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()


class ContactDetails(QtWidgets.QGroupBox):
    fn: QtWidgets.QLineEdit
    family: QtWidgets.QLineEdit
    given: QtWidgets.QLineEdit
    email: QtWidgets.QLineEdit
    tel: QtWidgets.QLineEdit

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Details")
        self.createWidgets()

    def createWidgets(self):
        # order
        self.fn = QtWidgets.QLineEdit(self)
        self.family = QtWidgets.QLineEdit(self)
        self.given = QtWidgets.QLineEdit(self)
        self.email = QtWidgets.QLineEdit(self)
        self.tel = QtWidgets.QLineEdit(self)
        # layout
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("FN:"), self.fn)
        layout.addRow(QtWidgets.QLabel("Family:"), self.family)
        layout.addRow(QtWidgets.QLabel("Given:"), self.given)
        layout.addRow(QtWidgets.QLabel("Email:"), self.email)
        layout.addRow(QtWidgets.QLabel("Tel.:"), self.tel)
        self.setLayout(layout)
        # attributes
        self.fn.setReadOnly(True)
        self.family.setReadOnly(True)
        self.given.setReadOnly(True)
        self.email.setReadOnly(True)
        self.tel.setReadOnly(True)

    def refresh_data(self, data):
        self.fn.setText(data.getFN())
        self.family.setText(data.getFamily())
        self.given.setText(data.getGiven())
        self.email.setText(data.getEmail())
        self.tel.setText(data.getTel())


class ContactsWidget(QtWidgets.QWidget):
    sources: ContactSources
    list: ContactList
    details: ContactDetails
    selectionChanged = QtCore.Signal(QtCore.QItemSelection)

    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.list.activated.connect(self.refresh_details)
        # model required
        # self.selModel = self.list.selectionModel()
        # self.selModel.selectionChanged.connect(self.selectionChanged)

    def createWidgets(self):
        # order
        splitter = QtWidgets.QSplitter(self)
        self.sources = ContactSources(splitter)
        self.list = ContactList(splitter)
        self.details = ContactDetails(splitter)
        # layout
        splitter.addWidget(self.sources)
        splitter.addWidget(self.list)
        splitter.addWidget(self.details)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(splitter)
        self.setLayout(layout)

    def refresh_details(self, idx):
        data = idx.model().getBack(idx)
        self.details.refresh_data(data)
