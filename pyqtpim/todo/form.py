"""Form to create/update VTODO item"""
from PySide2 import QtWidgets


class TodoForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TodoForm, self).__init__(parent)
        self.__createWidgets()
        self.setWindowTitle("Entry")

    def __createWidgets(self):
        # widgets
        self.summary = QtWidgets.QLineEdit()
        self.location = QtWidgets.QLineEdit()
        self.dtstart = QtWidgets.QDateTimeEdit()
        self.due = QtWidgets.QDateTimeEdit()
        self.description = QtWidgets.QTextEdit()

        self.list_combo = QtWidgets.QComboBox()
        self.list_combo.addItem("List1")
        self.list_combo.addItem("List2")

        self.cat_combo = QtWidgets.QComboBox()
        self.cat_combo.addItem("Cat1")
        self.cat_combo.addItem("Cat2")

        self.state_combo = QtWidgets.QComboBox()
        self.state_combo.addItem("State1")

        self.prio_combo = QtWidgets.QComboBox()
        self.prio_combo.addItem("Prio1")

        self.class_combo = QtWidgets.QComboBox()
        self.class_combo.addItem("Public")

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # layout
        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Summary", self.summary)
        layout.addRow("Location", self.location)
        layout.addRow("DTStart", self.dtstart)
        layout.addRow("Due", self.due)
        layout.addRow(self.description)
        layout.addRow(self.button_box)
        self.setLayout(layout)
