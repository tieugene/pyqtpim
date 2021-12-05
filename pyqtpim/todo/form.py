"""Form to create/update VTODO item"""
from PySide2 import QtWidgets, QtCore
# local
from .data import Todo


class TodoForm(QtWidgets.QDialog):
    """
    Create/Update form for VTODO
    :todo: pulldown info with:
    - created
    - dtstamp
    - modified
    - sequence
    - uid
    """
    f_list: QtWidgets.QComboBox
    f_category: QtWidgets.QLineEdit
    f_class: QtWidgets.QComboBox
    f_completed: QtWidgets.QDateTimeEdit
    f_description: QtWidgets.QPlainTextEdit
    f_dtstart: QtWidgets.QDateTimeEdit
    f_due: QtWidgets.QDateTimeEdit
    f_location: QtWidgets.QLineEdit
    f_percent: QtWidgets.QSpinBox
    f_priority: QtWidgets.QSlider
    f_status: QtWidgets.QComboBox
    f_summary: QtWidgets.QLineEdit
    f_url = QtWidgets.QLineEdit

    def __init__(self, parent=None):
        super(TodoForm, self).__init__(parent)
        self.__createWidgets()
        self.setWindowTitle("Entry")

    def __createWidgets(self):
        # = Widgets: =
        self.f_list = QtWidgets.QComboBox(self)
        self.f_list.addItem("List1")
        self.f_list.addItem("List2")
        # attach[]
        self.f_category = QtWidgets.QLineEdit(self)     # TODO: checkable combobox
        self.f_category.setClearButtonEnabled(True)
        self.f_class = QtWidgets.QComboBox(self)        # TODO: radio/slider?
        self.f_class.addItem('')
        self.f_class.addItem("Public")
        self.f_class.addItem("Private")
        self.f_class.addItem("Confidential")
        # comment[]
        self.f_completed = QtWidgets.QDateTimeEdit(self)    # date?
        self.f_completed.setCalendarPopup(True)
        # contact[]
        self.f_description = QtWidgets.QPlainTextEdit(self)
        self.f_dtstart = QtWidgets.QDateTimeEdit(self)  # FIXME: optional time
        self.f_dtstart.setCalendarPopup(True)
        self.f_due = QtWidgets.QDateTimeEdit(self)      # FIXME: optional time
        self.f_due.setCalendarPopup(True)
        self.f_location = QtWidgets.QLineEdit(self)
        self.f_location.setClearButtonEnabled(True)
        self.f_percent = QtWidgets.QSpinBox(self)       # TODO: +slider
        self.f_percent.setMaximum(100)
        self.f_priority = QtWidgets.QSlider(self)       # TODO: +QSpinBox
        self.f_priority.setOrientation(QtCore.Qt.Horizontal)
        self.f_priority.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.f_priority.setRange(0, 9)
        self.f_priority.setTickInterval(3)
        # relatedto
        # rrule
        self.f_status = QtWidgets.QComboBox(self)       # TODO: radio
        self.f_status.addItem('')               # _
        self.f_status.addItem("Needs Action")   # ?
        self.f_status.addItem("In Progress")    # ...
        self.f_status.addItem("Completed")      # v
        self.f_status.addItem("Cancelled")      # x
        self.f_summary = QtWidgets.QLineEdit(self)
        self.f_url = QtWidgets.QLineEdit(self)
        self.f_url.setClearButtonEnabled(True)
        # the end
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # = Layout: =
        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Summary", self.f_summary)
        layout.addRow("List", self.f_list)
        layout.addRow("Category", self.f_category)
        layout.addRow("Class", self.f_class)        # on demand
        layout.addRow("Priority", self.f_priority)
        layout.addRow("DTStart", self.f_dtstart)    # on demand
        layout.addRow("Due", self.f_due)
        layout.addRow("Status", self.f_status)
        layout.addRow("% complete", self.f_percent)
        layout.addRow("Completed", self.f_completed)
        layout.addRow("Location", self.f_location)  # on demand
        layout.addRow("URL", self.f_url)            # on demand
        layout.addRow("Description", self.f_description)
        # finish
        layout.addRow(self.button_box)
        self.setLayout(layout)

    # TODO: clear()

    def load(self, data: Todo):
        """Preload form with VTODO"""
        # self.f_list
        if v := data.getCategories():
            if isinstance(v, list):
                self.f_category.setText(', '.join(v))
            else:
                self.f_category.setText(v)
        if v := data.getClass():
            ...
        if v := data.getCompleted():
            ...
        self.f_description.setPlainText(data.getDescription())
        if v := data.getDTStart():
            ...
        if v := data.getDue():
            ...
        self.f_location.setText(data.getLocation())
        if v := data.getPercent():
            self.f_percent.setValue(v)
        if v := data.getPriority():
            self.f_priority.setValue(v)
        if v := data.getStatus():
            ...
        self.f_summary.setText(data.getSummary())
        self.f_url.setText(data.getURL())
