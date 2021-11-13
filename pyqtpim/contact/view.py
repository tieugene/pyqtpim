"""GUI representation of Contact things"""

from PySide2 import QtCore, QtGui, QtWidgets


class ContactsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.list.activated.connect(self.refresh_details)

    def createWidgets(self):
        # order
        self.sources = QtWidgets.QListView(self)
        self.list = QtWidgets.QTableView(self)
        self.details = QtWidgets.QWidget(self)
        self.details_fn_label = QtWidgets.QLabel(self.details)
        self.details_fn = QtWidgets.QLineEdit(self.details)
        self.details_family = QtWidgets.QLineEdit(self.details)
        self.details_given = QtWidgets.QLineEdit(self.details)
        self.details_email = QtWidgets.QLineEdit(self.details)
        self.details_tel = QtWidgets.QLineEdit(self.details)
        # layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.sources)
        self.horizontalLayout.addWidget(self.list)
        self.horizontalLayout.addWidget(self.details)
        # sizes
        self.details.setMinimumSize(QtCore.QSize(128, 100))
        self.details_fn.setGeometry(QtCore.QRect(20, 20, 100, 20))
        self.details_family.setGeometry(QtCore.QRect(20, 40, 100, 20))
        self.details_given.setGeometry(QtCore.QRect(20, 60, 100, 20))
        self.details_email.setGeometry(QtCore.QRect(20, 80, 100, 20))
        self.details_tel.setGeometry(QtCore.QRect(20, 100, 100, 20))
        # attributes
        self.details_fn.setReadOnly(True)
        self.details_family.setReadOnly(True)
        self.details_given.setReadOnly(True)
        self.details_email.setReadOnly(True)
        self.details_tel.setReadOnly(True)

    def refresh_details(self, idx):
        data = idx.model().getBack(idx)
        self.details_fn.setText(data.getFN())
        self.details_family.setText(data.getFamily())
        self.details_given.setText(data.getGiven())
        self.details_email.setText(data.getEmail())
        self.details_tel.setText(data.getTel())
