"""Form to create/update VTODO item

:todo: Class (radio/slider)
"""
# 1. std
import datetime
from typing import Optional, Union
# 2. PySide
from PySide2 import QtWidgets, QtCore
# 3. local
from .data import Todo


class CheckableDateTimeEdit(QtWidgets.QGroupBox):
    is_enabled: QtWidgets.QCheckBox
    is_timed: QtWidgets.QCheckBox
    f_date: QtWidgets.QDateEdit
    f_time: QtWidgets.QTimeEdit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_enabled = QtWidgets.QCheckBox()
        self.is_timed = QtWidgets.QCheckBox()
        self.f_date = QtWidgets.QDateEdit()
        self.f_date.setCalendarPopup(True)
        self.f_time = QtWidgets.QTimeEdit()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.is_enabled)
        layout.addWidget(self.f_date)
        layout.addWidget(self.is_timed)
        layout.addWidget(self.f_time)
        self.setLayout(layout)
        self.__reset()
        # signals
        self.is_enabled.stateChanged[int].connect(self.__switch_all)
        self.is_timed.stateChanged[int].connect(self.__switch_time)

    def __reset(self):
        self.is_enabled.setChecked(False)
        self.f_date.setEnabled(False)
        self.f_date.setEnabled(False)
        self.is_timed.setChecked(False)
        self.is_timed.setEnabled(False)
        self.f_time.setEnabled(False)

    def __switch_all(self, state: QtCore.Qt.CheckState):
        """
        :param state: 0=unchecked, 2=checked
        :return:
        """
        self.f_date.setEnabled(bool(state))
        self.is_timed.setEnabled(bool(state))
        self.f_time.setEnabled(bool(state) and self.is_timed.isChecked())

    def __switch_time(self, state: QtCore.Qt.CheckState):
        self.f_time.setEnabled(bool(state))

    def setData(self, data: Optional[Union[datetime.date, datetime.datetime]] = None):
        if data:
            self.is_enabled.setChecked(True)
            self.f_date.setEnabled(True)
            self.is_timed.setEnabled(True)
            if isinstance(data, datetime.datetime):
                self.f_date.setDate(data.date())
                self.is_timed.setChecked(True)
                self.f_time.setEnabled(True)
                self.f_time.setTime(data.time())
            else:
                self.f_date.setDate(data)

    def getData(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        if self.is_enabled.isChecked():
            if self.is_timed.isChecked():
                return datetime.datetime.combine(self.f_date.date(), self.f_time.time())
            else:
                return self.f_date.date()


class SlidedSpinBox(QtWidgets.QGroupBox):
    f_slider: QtWidgets.QSlider
    f_spinbox: QtWidgets.QSpinBox

    def __init__(self, v_max: int, parent=None):
        super().__init__(parent)
        self.f_slider = QtWidgets.QSlider()
        self.f_slider.setOrientation(QtCore.Qt.Horizontal)
        self.f_slider.setMaximum(v_max)
        self.f_spinbox = QtWidgets.QSpinBox()
        self.f_spinbox.setMaximum(v_max)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.f_slider)
        layout.addWidget(self.f_spinbox)
        self.setLayout(layout)
        # signals
        self.f_slider.valueChanged[int].connect(self._chg_slider)
        self.f_spinbox.valueChanged[int].connect(self._chg_spinbox)

    # @QtCore.Slot(int)
    def _chg_slider(self, v: int):
        self.f_spinbox.setValue(v)

    def _chg_spinbox(self, v: int):
        self.f_slider.setValue(v)

    def setData(self, data: int):
        if data is not None:
            self.f_slider.setValue(data)
            self.f_spinbox.setValue(data)

    def getData(self) -> int:
        return self.f_spinbox.value()


class PrioBox(SlidedSpinBox):
    def __init__(self, parent=None):
        super().__init__(9, parent)
        self.f_slider.setMaximum(3)
        self.f_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.f_slider.setTickInterval(1)

    @staticmethod
    def __spin2slide(v: int):
        return (0, 1, 1, 1, 1, 2, 3, 3, 3, 3)[v]

    def _chg_slider(self, v: int):
        # print("slider")
        if v == 0:
            self.f_spinbox.setValue(0)
        elif v == 1:
            if not (0 < self.f_spinbox.value() < 5):
                self.f_spinbox.setValue(1)
        elif v == 2:
            self.f_spinbox.setValue(5)
        elif v == 3:
            if not (5 < self.f_spinbox.value() < 9):
                self.f_spinbox.setValue(9)

    def _chg_spinbox(self, v: int):
        new_slide_v = self.__spin2slide(v)
        if self.f_slider.value() != new_slide_v:
            self.f_slider.setValue(new_slide_v)

    def setData(self, data: int):
        if data is not None:
            self.f_slider.setValue(self.__spin2slide(data))
            self.f_spinbox.setValue(data)

    def getData(self) -> int:
        return self.f_spinbox.value()


class TodoForm(QtWidgets.QDialog):
    """
    Create/Update form for VTODO
    :todo: popup/pulldown info: created, dtstamp, modified, sequence, uid
    :todo: select optional fields to show: class, ...
    :todo: set default values: priority, ..
    """
    f_list: QtWidgets.QComboBox
    f_category: QtWidgets.QLineEdit
    f_class: QtWidgets.QComboBox
    f_completed: CheckableDateTimeEdit
    f_description: QtWidgets.QPlainTextEdit
    f_dtstart: CheckableDateTimeEdit
    f_due: CheckableDateTimeEdit
    f_location: QtWidgets.QLineEdit
    f_percent: SlidedSpinBox   # Steps: TB/Evolution=1, Rainlendar=10, Reminder=x, OpenTodo=5
    f_priority: PrioBox
    f_status: QtWidgets.QComboBox
    f_summary: QtWidgets.QLineEdit
    f_url = QtWidgets.QLineEdit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__createWidgets()
        self.__setLayout()
        self.setWindowTitle("Entry")

    def __createWidgets(self):
        # = Widgets: =
        self.f_list = QtWidgets.QComboBox(self)
        self.f_list.addItem("List1")
        self.f_list.addItem("List2")
        # attach[]
        self.f_category = QtWidgets.QLineEdit(self)         # TODO: checkable combobox
        self.f_category.setClearButtonEnabled(True)
        self.f_class = QtWidgets.QComboBox(self)            # TODO: radio/slider?
        self.f_class.addItem('')
        self.f_class.addItem("Public")
        self.f_class.addItem("Private")
        self.f_class.addItem("Confidential")
        # comment[]
        self.f_completed = CheckableDateTimeEdit(self)
        # contact[]
        self.f_description = QtWidgets.QPlainTextEdit(self)
        self.f_dtstart = CheckableDateTimeEdit(self)
        self.f_due = CheckableDateTimeEdit(self)
        self.f_location = QtWidgets.QLineEdit(self)
        self.f_location.setClearButtonEnabled(True)
        self.f_percent = SlidedSpinBox(100, self)
        self.f_priority = PrioBox(self)
        # relatedto
        # rrule
        self.f_status = QtWidgets.QComboBox(self)           # TODO: radio?
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

    def __setLayout(self):
        """Bests: Evolution, RTM"""
        layout = QtWidgets.QFormLayout(self)    # FIME: not h-stretchable
        layout.addRow("List", self.f_list)
        layout.addRow("Summary", self.f_summary)
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
        self.f_completed.setData(data.getCompleted())
        self.f_description.setPlainText(data.getDescription())
        self.f_dtstart.setData(data.getDTStart())
        self.f_due.setData(data.getDue())
        self.f_location.setText(data.getLocation())
        self.f_percent.setData(data.getPercent())
        self.f_priority.setData(data.getPriority())
        if v := data.getStatus():
            ...
        self.f_summary.setText(data.getSummary())
        self.f_url.setText(data.getURL())
