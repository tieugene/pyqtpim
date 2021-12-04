"""Form to create/update VTODO item"""
from PySide2 import QtWidgets


class TodoForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TodoForm, self).__init__(parent)
        self.__createWidgets()
        self.setWindowTitle("Entry")

    def __createWidgets(self):
        """211204: 18 fields"""
        # widgets
        self.f_list = QtWidgets.QComboBox()
        self.f_list.addItem("List1")
        self.f_list.addItem("List2")
        # attach[]
        self.f_category = QtWidgets.QComboBox()
        self.f_category.addItem("Cat1")
        self.f_category.addItem("Cat2")
        self.f_class = QtWidgets.QComboBox()
        self.f_class.addItem("Public")
        # comment[]
        self.f_completed = QtWidgets.QDateTimeEdit()
        self.f_completed.setReadOnly(True)
        # contact[]
        self.f_created = QtWidgets.QDateTimeEdit()
        self.f_created.setReadOnly(True)
        self.f_description = QtWidgets.QTextEdit()
        self.f_dtstamp = QtWidgets.QDateTimeEdit()
        self.f_dtstamp.setReadOnly(True)
        self.f_dtstart = QtWidgets.QDateTimeEdit()
        self.f_due = QtWidgets.QDateTimeEdit()
        self.f_modified = QtWidgets.QDateTimeEdit()
        self.f_modified.setReadOnly(True)
        self.f_location = QtWidgets.QLineEdit()
        self.f_percent = QtWidgets.QSpinBox()
        self.f_percent.setMaximum(100)
        self.f_priority = QtWidgets.QComboBox()
        self.f_priority.addItem("---")
        self.f_priority.addItem("Low")
        self.f_priority.addItem("Mid")
        self.f_priority.addItem("High")
        # relatedto
        # rrule
        self.f_sequence = QtWidgets.QSpinBox()
        self.f_sequence.setMaximum(999999999)
        self.f_sequence.setReadOnly(True)
        self.f_status = QtWidgets.QComboBox()
        self.f_status.addItem("State1")
        self.f_summary = QtWidgets.QLineEdit()
        self.f_uid = QtWidgets.QLineEdit()
        self.f_uid.setReadOnly(True)
        self.f_url = QtWidgets.QLineEdit()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # layout
        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Summary", self.f_summary)
        layout.addRow("List", self.f_list)
        layout.addRow("Category", self.f_category)
        layout.addRow("Class", self.f_class)
        layout.addRow("Completed", self.f_completed)
        layout.addRow("Created", self.f_created)
        layout.addRow("DTStamp", self.f_dtstamp)
        layout.addRow("DTStart", self.f_dtstart)
        layout.addRow("Due", self.f_due)
        layout.addRow("Modified", self.f_modified)
        layout.addRow("Location", self.f_location)
        layout.addRow("% complete", self.f_percent)
        layout.addRow("Priority", self.f_priority)
        layout.addRow("Sequence", self.f_sequence)
        layout.addRow("Status", self.f_status)
        layout.addRow("UID", self.f_uid)
        layout.addRow("URL", self.f_url)
        layout.addRow("Description", self.f_description)
        layout.addRow(self.button_box)
        self.setLayout(layout)
