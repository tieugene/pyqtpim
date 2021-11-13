"""GUI representation of Contact things"""

from PySide2 import QtCore, QtWidgets


class ContactSources(QtWidgets.QListView):
    def __init__(self, parent):
        super().__init__(parent)


class ContactList(QtWidgets.QTableView):
    def __init__(self, parent):
        super().__init__(parent)


class ContactDetails(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.createWidgets()

    def createWidgets(self):
        # order
        self.fn_label = QtWidgets.QLabel(self)
        self.fn = QtWidgets.QLineEdit(self)
        self.family = QtWidgets.QLineEdit(self)
        self.given = QtWidgets.QLineEdit(self)
        self.email = QtWidgets.QLineEdit(self)
        self.tel = QtWidgets.QLineEdit(self)
        # sizes
        self.setMinimumSize(QtCore.QSize(128, 100))
        self.fn.setGeometry(QtCore.QRect(20, 20, 100, 20))
        self.family.setGeometry(QtCore.QRect(20, 40, 100, 20))
        self.given.setGeometry(QtCore.QRect(20, 60, 100, 20))
        self.email.setGeometry(QtCore.QRect(20, 80, 100, 20))
        self.tel.setGeometry(QtCore.QRect(20, 100, 100, 20))
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
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.list.activated.connect(self.refresh_details)

    def createWidgets(self):
        # order
        self.sources = ContactSources(self)
        self.list = ContactList(self)
        self.details = ContactDetails(self)
        # layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.sources)
        self.horizontalLayout.addWidget(self.list)
        self.horizontalLayout.addWidget(self.details)

    def refresh_details(self, idx):
        data = idx.model().getBack(idx)
        self.details.refresh_data(data)
