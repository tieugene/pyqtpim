"""GUI representation of Contact things"""

from PyQt5 import QtCore, QtWidgets
# 3. local
from common import EntryView, EntryListView, StoreListView, StoreModel
from .model import ContactListManagerModel, ContactModel


class ContactListManagerView(StoreListView):
    _model_cls = StoreModel
    _title = 'Contact list'

    def _empty_model(self) -> ContactListManagerModel:
        return ContactListManagerModel()


class ContactListView(EntryListView):
    def _empty_model(self) -> ContactModel:
        return ContactModel()


class ContactView(EntryView):
    fn: QtWidgets.QLineEdit
    family: QtWidgets.QLineEdit
    given: QtWidgets.QLineEdit
    email: QtWidgets.QLineEdit
    tel: QtWidgets.QLineEdit

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Details")
        self.__createWidgets()

    def __createWidgets(self):
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

    def setModel(self, model: QtCore.QStringListModel):
        """Setup mapper"""
        self.mapper.setModel(model)
        self.mapper.addMapping(self.fn, 0)
        self.mapper.addMapping(self.family, 1)
        self.mapper.addMapping(self.given, 2)
        self.mapper.addMapping(self.email, 3)
        self.mapper.addMapping(self.tel, 4)

    def clean(self):
        # print("Details clean call")
        self.fn.clear()
        self.family.clear()
        self.given.clear()
        self.email.clear()
        self.tel.clear()


class ContactsWidget(QtWidgets.QWidget):
    sources: ContactListManagerView
    list: ContactListView
    details: ContactView

    def __init__(self):
        super().__init__()
        self.__createWidgets()

    def __createWidgets(self):
        # order
        splitter = QtWidgets.QSplitter(self)
        self.details = ContactView(splitter)
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
    dieday: QtWidgets.QDateEdit  # !new
    dielocation: QtWidgets.QLineEdit
    anniversary: QtWidgets.QDateEdit  # marriage (годовщина?)
    sex: QtWidgets.QComboBox  # enum:5
    # 3. Delivery Addressing            # TODO: (?prio:bool, type:h/w/+, subj
    adr_pobox: QtWidgets.QLineEdit  # Post Office Box; should be empty
    adr_ext: QtWidgets.QLineEdit  # Extended address (appartment, suite); should be empty
    adr_street: QtWidgets.QLineEdit  # incl. build
    adr_locality: QtWidgets.QLineEdit  # e.g. city
    adr_region: QtWidgets.QLineEdit  # e.g. state, province
    adr_code: QtWidgets.QLineEdit  # postal code
    adr_country: QtWidgets.QComboBox
    # 4. Communication
    tel: list[QtWidgets.QLineEdit]  # TODO: (?prio:bool, ?type:enum, tel:str)
    email: list[QtWidgets.QLineEdit]  # TODO: (?prio:bool, ?type:w/h/o), email:str)
    impp: list[QtWidgets.QLineEdit]  # TODO: (?prio:bool, type:skype/jabber/gtalk/qq, account:str)
    # lang: QtWidgets.QComboBox
    # 5. Geographical
    # tz
    # geo
    # 6. Organizational
    title: QtWidgets.QLineEdit
    role: QtWidgets.QLineEdit
    # logo
    org: QtWidgets.QLineEdit
    member: str  # for KIND=group only
    # related
    # 7. Explanatory
    categories: QtWidgets.QLineEdit  # csv
    note: QtWidgets.QPlainTextEdit
    # prodid
    # rev
    # sound
    # uid
    url: list[QtWidgets.QLineEdit]  # TODO: (?prio:bool, type:w/h/o, subj:str)
    events: list[QtWidgets.QLineEdit]  # TODO: (?prio:bool, date:date, subj:str)
    prefered_mail: str  # plaintext/html/unknown
    pubkeys: list[QtWidgets.QLineEdit]  # TODO: add prio:bool; not works
