"""Form to create/update VTODO item"""
# 1. std
import datetime
from typing import Optional, Union, Any
# 2. PySide
from PySide2 import QtWidgets, QtCore, QtSql
# 3. local
from .data import VObjTodo
from . import enums


class ListEdit(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = QtSql.QSqlTableModel()
        model.setTable("store")
        model.select()
        self.setModel(model)
        self.setModelColumn(model.fieldIndex('name'))

    def setData(self, list_id: int):
        """FIXME: dirty"""
        m = self.model()
        for i in range(m.rowCount()):
            if m.data(m.index(i, 0)) == list_id:
                self.setCurrentIndex(i)
                break

    def getData(self) -> int:
        """Return store_id selected"""
        return self.model().data(self.model().index(self.currentIndex(), 0))


class CheckableDateTimeEdit(QtWidgets.QWidget):
    is_enabled: QtWidgets.QCheckBox
    f_datetime: QtWidgets.QDateTimeEdit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.is_enabled = QtWidgets.QCheckBox()
        self.f_datetime = QtWidgets.QDateTimeEdit()
        self.f_datetime.setCalendarPopup(True)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.is_enabled)
        layout.addWidget(self.f_datetime)
        self.setLayout(layout)
        self.__reset()
        # signals
        self.is_enabled.stateChanged[int].connect(self.__switch_all)

    def __reset(self):
        self.is_enabled.setChecked(False)
        self.f_datetime.setEnabled(False)

    def __switch_all(self, state: QtCore.Qt.CheckState):
        """
        :param state: 0=unchecked, 2=checked
        :return:
        """
        self.f_datetime.setEnabled(bool(state))

    def setData(self, data: Optional[datetime.datetime] = None):
        if data:
            self.is_enabled.setChecked(True)
            self.f_datetime.setEnabled(True)
            self.f_datetime.setDateTime(data)

    def getData(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        if self.is_enabled.isChecked():
            return self.f_datetime.datetime().toPython()


class CheckableDateAndTimeEdit(QtWidgets.QWidget):
    is_enabled: QtWidgets.QCheckBox
    is_timed: QtWidgets.QCheckBox
    f_date: QtWidgets.QDateEdit
    f_time: QtWidgets.QTimeEdit
    t_tz: datetime.tzinfo   # TODO: handle tz

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.is_enabled = QtWidgets.QCheckBox()
        self.is_timed = QtWidgets.QCheckBox()
        self.f_date = QtWidgets.QDateEdit()
        self.f_date.setCalendarPopup(True)
        self.f_time = QtWidgets.QTimeEdit()
        self.t_tz = None
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
                self.t_tz = data.tzinfo
                # print(self.t_tz)
            else:  # date
                self.f_date.setDate(data)

    def getData(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        if self.is_enabled.isChecked():
            if self.is_timed.isChecked():
                return datetime.datetime.combine(
                    self.f_date.date().toPython(),
                    self.f_time.time().toPython(),
                    tzinfo=self.t_tz
                )
            else:
                return self.f_date.date().toPython()


class SlidedSpinBox(QtWidgets.QWidget):
    f_slider: QtWidgets.QSlider
    f_spinbox: QtWidgets.QSpinBox

    def __init__(self, v_max: int, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
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


class PrioWidget(SlidedSpinBox):
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


class SpecialCombo(QtWidgets.QComboBox):
    _data2idx: dict[Any, int]
    _idx2data: tuple

    def __init__(self, items: tuple, parent=None):
        super().__init__(parent)
        self.addItems(items)

    def setData(self, data):
        self.setCurrentIndex(self._data2idx[data])

    def getData(self) -> Any:
        return self._idx2data[self.currentIndex()]


class ClassCombo(SpecialCombo):
    _data2idx: dict[enums.EClass, int] = {
        None: 0,
        enums.EClass.Public: 1,
        enums.EClass.Private: 2,
        enums.EClass.Confidential: 3,
    }
    _idx2data = (
        None,
        enums.EClass.Public,
        enums.EClass.Private,
        enums.EClass.Confidential,
    )

    def __init__(self, parent=None):
        super().__init__(('', "Public", "Private", "Confidential"), parent)


class StatusCombo(SpecialCombo):
    _data2idx: dict[enums.EStatus, int] = {
        None: 0,
        enums.EStatus.NeedsAction: 1,
        enums.EStatus.InProcess: 2,
        enums.EStatus.Completed: 3,
        enums.EStatus.Cancelled: 4
    }
    _idx2data = (
        None,
        enums.EStatus.NeedsAction,
        enums.EStatus.InProcess,
        enums.EStatus.Completed,
        enums.EStatus.Cancelled
    )

    def __init__(self, parent=None):
        super().__init__(('', "Needs Action", "In Progress", "Completed", "Cancelled"), parent)


class TodoForm(QtWidgets.QDialog):
    """
    Create/Update form for VTODO
    :todo: popup/pulldown info: created, dtstamp, modified, sequence, uid
    :todo: select optional fields to show: class, ...
    :todo: set default values: priority, ...
    """
    f_list: QtWidgets.QComboBox
    f_category: QtWidgets.QLineEdit
    f_class: ClassCombo
    f_completed: CheckableDateTimeEdit
    f_description: QtWidgets.QPlainTextEdit
    f_dtstart: CheckableDateAndTimeEdit
    f_due: CheckableDateAndTimeEdit
    f_location: QtWidgets.QLineEdit
    f_percent: SlidedSpinBox   # Steps: TB/Evolution=1, Rainlendar=10, Reminder=x, OpenTodo=5
    f_priority: PrioWidget
    f_status: StatusCombo
    f_summary: QtWidgets.QLineEdit
    f_url = QtWidgets.QLineEdit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__createWidgets()
        self.__setLayout()
        self.f_summary.setFocus()
        self.setWindowTitle("Entry")

    def __createWidgets(self):
        # = Widgets: =
        self.f_list = ListEdit(self)
        # attach[]
        self.f_category = QtWidgets.QLineEdit(self)         # TODO: checkable combobox
        self.f_category.setClearButtonEnabled(True)
        self.f_class = ClassCombo(self)                     # TODO: radio/slider?
        # comment[]
        self.f_completed = CheckableDateTimeEdit(self)
        # contact[]
        self.f_description = QtWidgets.QPlainTextEdit(self)
        self.f_dtstart = CheckableDateAndTimeEdit(self)
        self.f_due = CheckableDateAndTimeEdit(self)
        self.f_location = QtWidgets.QLineEdit(self)
        self.f_location.setClearButtonEnabled(True)
        self.f_percent = SlidedSpinBox(100, self)
        self.f_priority = PrioWidget(self)
        # relatedto
        # rrule
        self.f_status = StatusCombo(self)                   # TODO: radio?
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

    def clear(self):    # TODO: clear old values for newly creating entry
        ...

    def load(self, data: VObjTodo, list_id: int):
        """Preload form with VTODO"""
        self.f_list.setData(list_id)
        if v := data.getCategories():
            if isinstance(v, list):
                self.f_category.setText(', '.join(v))
            else:
                self.f_category.setText(v)
        self.f_class.setData(data.getClass())
        self.f_completed.setData(data.getCompleted())
        self.f_description.setPlainText(data.getDescription())
        self.f_dtstart.setData(data.getDTStart())
        self.f_due.setData(data.getDue())
        self.f_location.setText(data.getLocation())
        self.f_percent.setData(data.getPercent())
        self.f_priority.setData(data.getPriority())
        self.f_status.setData(data.getStatus())
        self.f_summary.setText(data.getSummary())
        self.f_url.setText(data.getURL())


def form2rec_upd(form: TodoForm, obj: VObjTodo, rec: QtSql.QSqlRecord) -> bool:
    """*Update* Todo object and record from form.
    :return: True if anythong changed and record must be saved.

    :todo: unify and/or hide into Entry setX()
    """
    obj_chgd = rec_chgd = False
    v_new = form.f_list.getData()
    if v_new != rec.value('store_id'):
        rec.setValue('store_id', v_new)
        rec_chgd = True
    # - cat
    if v_new := form.f_category.text():
        v_new = [s.strip() for s in v_new.split(',')]
        v_new.sort()
    else:   # empty list
        v_new = None
    v_old = obj.getCategories()
    if v_old != v_new:  # compare 0/1/2+ x 0/1/2+
        obj.setCategories(v_new)
        # TODO: db cats
        obj_chgd = True
    # - class (combo)
    v_new = form.f_class.getData()
    if obj.getClass() != v_new:
        obj.setClass(v_new)
        # no db
        obj_chgd = True
    # - completed
    v_new = form.f_completed.getData()
    if obj.getCompleted() != v_new:
        obj.setCompleted(v_new)
        if v_new:
            rec.setValue('completed', v_new.isoformat())
        else:
            rec.setNull('completed')
        obj_chgd = rec_chgd = True
    # - description
    v_new = form.f_description.toPlainText() or None
    if obj.getDescription() != v_new:
        obj.setDescription(v_new)
        # no db
        obj_chgd = True
    # - dtstart
    v_new = form.f_dtstart.getData()
    if obj.getDTStart() != v_new:
        obj.setDTStart(v_new)
        if v_new:
            rec.setValue('dtstart', v_new.isoformat())
        else:
            rec.setNull('dtstart')
        obj_chgd = rec_chgd = True
    # - due
    v_new = form.f_due.getData()
    if obj.getDue() != v_new:
        obj.setDue(v_new)
        if v_new:
            rec.setValue('due', v_new.isoformat())
        else:
            rec.setNull('due')
        obj_chgd = rec_chgd = True
    # - location
    v_new = form.f_location.text() or None
    if obj.getLocation() != v_new:
        obj.setLocation(v_new)
        if v_new:
            rec.setValue('location', v_new)
        else:
            rec.setNull('location')
        obj_chgd = rec_chgd = True
    # - percent
    v_new = form.f_percent.getData()
    v_old = obj.getPercent()    # 0+
    if v_old != v_new and not (v_new == 0 and v_old is None):   # FIXME: dirty hack
        obj.setPercent(v_new)
        if v_new is not None:
            rec.setValue('progress', v_new)
        else:
            rec.setNull('progress')
        obj_chgd = rec_chgd = True
    # - priority
    v_new = form.f_priority.getData()
    v_old = obj.getPriority()
    if v_old != v_new and not (v_new == 0 and v_old is None):
        obj.setPriority(v_new)
        if v_new is not None:
            rec.setValue('priority', v_new)
        else:
            rec.setNull('priority')
        obj_chgd = rec_chgd = True
    # - status (combo)
    v_new = form.f_status.getData()
    if obj.getStatus() != v_new:
        obj.setStatus(v_new)
        if v_new:
            rec.setValue('status', v_new.value)
        else:
            rec.setNull('status')
        obj_chgd = rec_chgd = True
    # - summary
    v_new = form.f_summary.text() or None
    if obj.getSummary() != v_new:
        obj.setSummary(v_new)
        if v_new:
            rec.setValue('summary', v_new)
        else:
            rec.setNull('summary')
        obj_chgd = rec_chgd = True
    # - url
    v_new = form.f_url.text() or None
    if obj.getURL() != v_new:
        obj.setURL(v_new)
        # no db
        obj_chgd = True
    # final
    if obj_chgd:
        obj.updateStamps()
        rec.setValue('modified', obj.getLastModified().isoformat())
        rec.setValue('body', obj.serialize())
        rec_chgd = True
    return rec_chgd


def form2obj(form: TodoForm) -> (VObjTodo, int):
    obj = VObjTodo()
    if v_new := form.f_category.text():
        v_new = [s.strip() for s in v_new.split(',')]
        v_new.sort()
        obj.setCategories(v_new)
    if v_new := form.f_class.getData():
        obj.setClass(v_new)
    if v_new := form.f_completed.getData():
        obj.setCompleted(v_new)
    if v_new := form.f_description.toPlainText():
        obj.setDescription(v_new)
    if v_new := form.f_dtstart.getData():
        obj.setDTStart(v_new)
    if v_new := form.f_due.getData():
        obj.setDue(v_new)
    if v_new := form.f_location.text():
        obj.setLocation(v_new)
    if v_new := form.f_percent.getData():
        obj.setPercent(v_new)
    if v_new := form.f_priority.getData():
        obj.setPriority(v_new)
    if v_new := form.f_status.getData():
        obj.setStatus(v_new)
    if v_new := form.f_summary.text():
        obj.setSummary(v_new)
    if v_new := form.f_url.text():
        obj.setURL(v_new)
    obj.updateStamps()
    return obj, form.f_list.getData()
