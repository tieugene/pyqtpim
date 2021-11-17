"""GUI representation of Contact things
:todo: link sources>list>details as buddies or attributes
"""
import os.path

from PySide2 import QtCore, QtWidgets
# 3. local
from .model import ContactListManagerModel, ContactListModel
from .entry import Contact
from .collection import ContactList


class ContactDetailWidget(QtWidgets.QGroupBox):
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

    def refresh(self, data: Contact = None):
        if data:
            self.fn.setText(data.FN)
            self.family.setText(data.Family)
            self.given.setText(data.Given)
            self.email.setText(data.EmailList)
            self.tel.setText(data.TelList)
        else:
            self.fn.clear()
            self.family.clear()
            self.given.clear()
            self.email.clear()
            self.tel.clear()


class ContactListView(QtWidgets.QTableView):
    __details: ContactDetailWidget

    def __init__(self, parent, dependant: ContactDetailWidget):
        super().__init__(parent)
        self.__details = dependant
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        # self.setEditTriggers(self.NoEditTriggers)
        # self.setSortingEnabled(True) # requires sorting itself
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        self.setModel(ContactListModel())
        # signals
        self.activated.connect(self.refresh_details)
        self.selectionModel().selectionChanged.connect(self.refresh_details)

    def refresh(self, data: ContactList = None):
        self.model().switch_data(data)
        self.__details.refresh()

    def refresh_details(self, selection: QtCore.QItemSelection):
        """Fully refresh details widget on CL selection changed"""
        if idx_list := selection.indexes():
            i = idx_list[0].row()
            c = self.model().item(i)
            self.__details.refresh(c)
        else:
            print("No contact selected")


class ContactListManagerView(QtWidgets.QListView):
    __list: ContactListView

    def __init__(self, parent, dependant: ContactListView):
        super().__init__(parent)
        self.__list = dependant
        self.setSelectionMode(self.SingleSelection)
        self.setModel(ContactListManagerModel())
        # set model required
        self.selectionModel().selectionChanged.connect(self.refresh_list)

    def itemAdd(self):
        """Add new CL."""
        dialog = ContactListCUDialog()
        while dialog.exec_():
            name = dialog.name
            path = dialog.path
            # check values
            # - name is uniq
            if self.model().findByName(name):
                QtWidgets.QMessageBox.warning(self, "Duplicated 'name'", f"CL with name '{name}' already registered")
                continue
            # - path is uniq
            if self.model().findByPath(path):
                QtWidgets.QMessageBox.warning(self, "Duplicated 'path'", f"CL with path '{path}' already registered")
                continue
            # - path exists and is dir
            if not os.path.isdir(path):
                QtWidgets.QMessageBox.warning(self, "Wrong 'path'", f"Path '{path}' is not dir or not exists")
                continue
            self.model().itemAdd(name, path)    # update UI
            break

    def itemEdit(self):
        indexes = self.selectionModel().selectedRows()
        if not indexes:
            return
        idx = indexes[0]
        i = idx.row()
        cl = self.model().item(i)
        dialog = ContactListCUDialog(cl.name, cl.path)
        while dialog.exec_():
            name = dialog.name
            path = dialog.path
            # check values
            # - changed
            if name == cl.name and path == cl.path:  # nothing changed
                break
            # - name is uniq but not this
            if self.model().findByName(name, i):
                QtWidgets.QMessageBox.warning(self, "Traversal 'name'", f"There is another CL with name '{name}'")
                continue
            # - path is uniq but not this
            if self.model().findByPath(path, i):
                QtWidgets.QMessageBox.warning(self, "Traversal 'path'", f"There is another CL with path '{path}'")
                continue
            # - path exists and is dir
            if not os.path.isdir(path):
                QtWidgets.QMessageBox.warning(self, "Wrong 'path'", f"Path '{path}' is not dir or not exists")
                continue
            self.model().itemUpdate(idx, name, path)    # update UI
            break

    def itemDel(self):
        indexes = self.selectionModel().selectedRows()
        for index in indexes:
            i = index.row()
            name = self.model().item(i).name
            if QtWidgets.QMessageBox.question(self, "Deleting CL", f"Are you sure to delete '{name}'")\
                    == QtWidgets.QMessageBox.StandardButton.Yes:
                self.model().itemDel(i)

    def itemInfo(self):
        indexes = self.selectionModel().selectedRows()
        if not indexes:
            return
        idx = indexes[0]
        cl = self.model().item(idx.row())
        QtWidgets.QMessageBox.information(self, "CL info",
                                          f"Addressbook info:\n"
                                          f"Name: {cl.name}\n"
                                          f"Path: {cl.path}\n"
                                          f"Records: {cl.size}")

    def refresh_list(self, selection: QtCore.QItemSelection):
        """Fully refresh CL widget on CLM selection changed"""
        if idx_list := selection.indexes():
            i = idx_list[0].row()
            cl = self.model().item(i)
            self.__list.refresh(cl)
        else:
            # print("No list selected")
            self.__list.refresh()


class ContactsWidget(QtWidgets.QWidget):
    sources: ContactListManagerView
    list: ContactListView
    details: ContactDetailWidget

    def __init__(self):
        super().__init__()
        self.createWidgets()

    def createWidgets(self):
        # order
        splitter = QtWidgets.QSplitter(self)
        self.details = ContactDetailWidget(splitter)
        self.list = ContactListView(splitter, self.details)
        self.sources = ContactListManagerView(splitter, self.list)
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

# --- dialogs ----


class ContactListCUDialog(QtWidgets.QDialog):
    """ A dialog to add (Create) or edit (Update) Addressbook."""
    nameText: QtWidgets.QLineEdit
    pathText: QtWidgets.QLineEdit

    def __init__(self, name: str = None, path: str = None):
        super().__init__()
        name_label = QtWidgets.QLabel("Name")
        path_label = QtWidgets.QLabel("Path")
        path_button = QtWidgets.QPushButton("...")
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.nameText = QtWidgets.QLineEdit()
        self.pathText = QtWidgets.QLineEdit()

        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.nameText, 0, 1, 1, 2)
        grid.addWidget(path_label, 1, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid.addWidget(self.pathText, 1, 1)
        grid.addWidget(path_button, 1, 2)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.setWindowTitle("Add a Contact Source")
        path_button.clicked.connect(self.browse_dir)
        button_box.accepted.connect(self.chk_values)
        button_box.rejected.connect(self.reject)

        if name:
            self.nameText.setText(name)
        if path:
            self.pathText.setText(path)

    def browse_dir(self):
        # TODO: set starting path
        if directory := QtCore.QDir.toNativeSeparators(
                QtWidgets.QFileDialog.getExistingDirectory(self, "Select dir", QtCore.QDir.currentPath())):
            self.pathText.setText(directory)

    def chk_values(self):
        if self.name and self.path:
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Empty values", "As 'name' as 'path' must not be empty")

    @property
    def name(self):
        return self.nameText.text()

    @property
    def path(self):
        return self.pathText.text()


class ContactCUDialog(QtWidgets.QDialog):
    # 1. General
    kind: QtWidgets.QComboBox
    # 2.  Identification
    fn: QtWidgets.QLineEdit
    n_pfx: QtWidgets.QLineEdit
    n_last: QtWidgets.QLineEdit
    n_first: QtWidgets.QLineEdit
    n_middle: QtWidgets.QLineEdit
    n_sfx: QtWidgets.QLineEdit
    nickname: QtWidgets.QLineEdit
    # photo: QtWidgets.Q
    bday: QtWidgets.QDateEdit
    dieday: QtWidgets.QDateEdit    # !new
    dielocation: QtWidgets.QLineEdit
    anniversary: QtWidgets.QDateEdit  # marriage (годовщина?)
    sex: QtWidgets.QComboBox          # enum:5
    # 3. Delivery Addressing            # TODO: (?prio:bool, type:h/w/+, subj
    adr_pobox: QtWidgets.QLineEdit      # Post Office Box; should be empty
    adr_ext: QtWidgets.QLineEdit        # Extended address (appartment, suite); should be empty
    adr_street: QtWidgets.QLineEdit     # incl. build
    adr_locality: QtWidgets.QLineEdit   # e.g. city
    adr_region: QtWidgets.QLineEdit     # e.g. state, province
    adr_code: QtWidgets.QLineEdit       # postal code
    adr_country: QtWidgets.QComboBox
    # 4. Communication
    tel: list[QtWidgets.QLineEdit]      # TODO: (?prio:bool, ?type:enum, tel:str)
    email: list[QtWidgets.QLineEdit]    # TODO: (?prio:bool, ?type:w/h/o), email:str)
    impp: list[QtWidgets.QLineEdit]     # TODO: (?prio:bool, type:skype/jabber/gtalk/qq, account:str)
    # lang: QtWidgets.QComboBox
    # 5. Geographical
    # tz
    # geo
    # 6. Organizational
    title: QtWidgets.QLineEdit
    role: QtWidgets.QLineEdit
    # logo
    org: QtWidgets.QLineEdit
    member: str         # for KIND=group only
    # related
    # 7. Explanatory
    categories: QtWidgets.QLineEdit     # csv
    note: QtWidgets.QPlainTextEdit
    # prodid
    # rev
    # sound
    # uid
    url: list[QtWidgets.QLineEdit]      # TODO: (?prio:bool, type:w/h/o, subj:str)
    events: list[QtWidgets.QLineEdit]   # TODO: (?prio:bool, date:date, subj:str)
    prefered_mail: str  # plaintext/html/unknown
    pubkeys: list[QtWidgets.QLineEdit]  # TODO: add prio:bool; not works
