"""GUI representation of Contact things
:todo: link sources>list>details as buddies or attributes
"""

from PySide2 import QtCore, QtWidgets
# 3. local
from .model import ContactListManagerModel, ContactListModel


class ContactSources(QtWidgets.QListView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setSelectionMode(self.SingleSelection)
        self.setModel(ContactListManagerModel())

    def addEntry(self):
        addDialog = AddDialogWidget()
        if addDialog.exec_():
            name = addDialog.name
            path = addDialog.path

    def editEntry(self):
        ...

    def delEntry(self):
        ...


class ContactList(QtWidgets.QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        # self.setEditTriggers(self.NoEditTriggers)
        # self.setSortingEnabled(True) # requires sorting itself
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        self.setModel(ContactListModel())


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
        # set model required
        # refresh list
        self.sources.selectionModel().selectionChanged.connect(self.refresh_list)
        # self.sources.selectionModel().emitSelectionChanged()
        # refresh details
        self.list.selectionModel().selectionChanged.connect(self.refresh_details)

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

    def refresh_list(self, selection: QtCore.QItemSelection):
        if idx_list := selection.indexes():
            self.list.model().beginResetModel()
            i = idx_list[0].row()
            cl = self.sources.model().clm[i][1]
            self.list.model().cl = cl
            self.list.model().endResetModel()
            # print(cl)
        else:
            print("No list selected")

    def refresh_details(self, selection: QtCore.QItemSelection):
        if idx_list := selection.indexes():
            # c = idx.model().getBack(idx)
            i = idx_list[0].row()
            c = self.list.model().cl[i]
            self.details.refresh_data(c)
        else:
            print("No contact selected")


class ContactSourceAdd(QtWidgets.QDialog):
    ...

# ---- dialogs ----


class AddDialogWidget(QtWidgets.QDialog):
    """ A dialog to add a new address to the addressbook. """
    def __init__(self, parent=None):
        super().__init__(parent)
        nameLabel = QtWidgets.QLabel("Name")
        pathLabel = QtWidgets.QLabel("Path")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.nameText = QtWidgets.QLineEdit()
        self.pathText = QtWidgets.QLineEdit()
        # self.pathButton = QtWidgets.QButton()   # link QFileDialg.getExistingDirectory()

        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(1, 2)
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(self.nameText, 0, 1)
        grid.addWidget(pathLabel, 1, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid.addWidget(self.pathText, 1, 1, QtCore.Qt.AlignLeft)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

        self.setWindowTitle("Add a Contact Source")
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    @property
    def name(self):
        return self.nameText.text()

    @property
    def path(self):
        return self.pathText.text()
