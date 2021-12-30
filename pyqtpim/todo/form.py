"""Form to create/update VTODO item"""
# 1. std
import datetime
from typing import Optional, Union, Any
# 2. PySide
from PySide2 import QtWidgets, QtCore
# 3. 3rds
import vobject
import dateutil
# 4. local
from .data import TodoVObj, TodoStore
from . import enums, model


def _tz_local():
    # return dateutil.tz.tz.tzlocal()     # 'MSK'
    return dateutil.tz.gettz()


def _tz_utc():
    return vobject.icalendar.utc


class StoreWidget(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(model.store_model)

    def setData(self, store: TodoStore):
        self.setCurrentIndex(self.model().item_find(store))

    def getData(self) -> TodoStore:
        return self.model().item_get(self.currentIndex())


class CheckableDateTimeEdit(QtWidgets.QWidget):
    """Fixme: UTC<>local"""
    is_enabled: QtWidgets.QCheckBox
    f_datetime: QtWidgets.QDateTimeEdit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.is_enabled = QtWidgets.QCheckBox(self)
        self.f_datetime = QtWidgets.QDateTimeEdit(self)
        self.f_datetime.setCalendarPopup(True)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.is_enabled)
        layout.addWidget(self.f_datetime)
        self.setLayout(layout)
        self.__reset()
        # signals
        self.is_enabled.stateChanged[int].connect(self.__switch_all)

    def __reset(self):
        now = datetime.datetime.now().replace(microsecond=0)
        self.is_enabled.setChecked(False)
        self.f_datetime.setEnabled(False)
        self.f_datetime.setDateTime(now)

    def __switch_all(self, state: QtCore.Qt.CheckState):
        """
        :param state: 0=unchecked, 2=checked
        :return:
        """
        self.f_datetime.setEnabled(bool(state))

    def setData(self, v: Optional[datetime.datetime] = None):
        if v:
            self.is_enabled.setChecked(True)
            self.f_datetime.setEnabled(True)
            self.f_datetime.setDateTime(v)
        else:
            self.__reset()

    def getData(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        if self.is_enabled.isChecked():
            return self.f_datetime.dateTime().toPython().replace(microsecond=0)


class CheckableDateAndTimeEdit(QtWidgets.QWidget):
    is_enabled: QtWidgets.QCheckBox
    is_timed: QtWidgets.QCheckBox
    is_tzed: QtWidgets.QCheckBox
    f_date: QtWidgets.QDateEdit
    f_time: QtWidgets.QTimeEdit
    t_tz: datetime.tzinfo  # TODO: handle tz
    l_tz: QtWidgets.QLabel

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.is_enabled = QtWidgets.QCheckBox(self)
        self.is_timed = QtWidgets.QCheckBox(self)
        self.is_tzed = QtWidgets.QCheckBox(self)
        self.f_date = QtWidgets.QDateEdit(self)
        self.f_time = QtWidgets.QTimeEdit(self)
        self.l_tz = QtWidgets.QLabel(self)
        self.f_date.setCalendarPopup(True)
        self.t_tz = datetime.timezone.utc
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.is_enabled)
        layout.addWidget(self.f_date)
        layout.addWidget(self.is_timed)
        layout.addWidget(self.f_time)
        layout.addWidget(self.is_tzed)
        layout.addWidget(self.l_tz)
        self.setLayout(layout)
        self.__reset()
        # signals
        self.is_enabled.stateChanged[int].connect(self.__switch_all)
        self.is_timed.stateChanged[int].connect(self.__switch_time)

    def __reset(self):
        now = datetime.datetime.now().replace(microsecond=0).astimezone()
        self.t_tz = _tz_local()
        # self.t_tz = dateutil.tz.tz._tzicalvtz(now.tzinfo) - bad idea
        # print("Init:", type(self.t_tz))
        # pprint.pprint(self.t_tz.__dict__)
        self.is_enabled.setChecked(False)
        self.f_date.setDate(now.date())
        self.f_date.setEnabled(False)
        self.is_timed.setChecked(False)
        self.is_timed.setEnabled(False)
        self.f_time.setEnabled(False)
        self.f_time.setTime(now.time())
        self.is_tzed.setChecked(False)
        self.is_tzed.setEnabled(False)
        # self.l_tz.setText(str(self.t_tz))  # FIXME:
        self.l_tz.setText(self.t_tz._ttinfo_std.abbr)

    def __switch_all(self, state: QtCore.Qt.CheckState):
        """
        :param state: 0=unchecked, 2=checked
        :return:
        """
        self.f_date.setEnabled(bool(state))
        self.is_timed.setEnabled(bool(state))
        self.f_time.setEnabled(bool(state) and self.is_timed.isChecked())
        self.is_tzed.setEnabled(bool(state) and self.is_timed.isChecked())

    def __switch_time(self, state: QtCore.Qt.CheckState):
        self.f_time.setEnabled(bool(state))
        self.is_tzed.setEnabled(bool(state))

    def setData(self, v: Optional[Union[datetime.date, datetime.datetime]] = None):
        if v:
            self.is_enabled.setChecked(True)
            self.f_date.setEnabled(True)
            self.is_timed.setEnabled(True)
            if isinstance(v, datetime.datetime):
                self.f_date.setDate(v.date())
                self.is_timed.setChecked(True)
                self.f_time.setEnabled(True)
                self.f_time.setTime(v.time())
                if v.tzinfo:
                    self.is_tzed.setChecked(True)
                    self.t_tz = v.tzinfo  # real/None (naive); type=dateutil.tz.tz._tzicalvtz
                    self.l_tz.setText(self.t_tz._tzid)
            else:  # date
                self.f_date.setDate(v)
        else:
            self.__reset()

    def getData(self) -> Optional[Union[datetime.date, datetime.datetime]]:
        if self.is_enabled.isChecked():
            if self.is_timed.isChecked():
                return datetime.datetime.combine(
                    self.f_date.date().toPython(),
                    self.f_time.time().toPython(),
                    tzinfo=self.t_tz if self.is_tzed.isChecked() else None
                ).replace(microsecond=0)
            else:
                return self.f_date.date().toPython()


class SlidedSpinBox(QtWidgets.QWidget):
    is_enabled: QtWidgets.QCheckBox
    f_slider: QtWidgets.QSlider
    f_spinbox: QtWidgets.QSpinBox

    def __init__(self, v_max: int, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.is_enabled = QtWidgets.QCheckBox(self)
        self.f_slider = QtWidgets.QSlider(self)
        self.f_spinbox = QtWidgets.QSpinBox(self)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.is_enabled)
        layout.addWidget(self.f_slider)
        layout.addWidget(self.f_spinbox)
        self.setLayout(layout)
        self.f_slider.setOrientation(QtCore.Qt.Horizontal)
        self.f_spinbox.setMaximum(v_max)
        # signals
        self.is_enabled.stateChanged[int].connect(self.__chg_enabled)

    def __reset(self):
        self.f_slider.setValue(0)
        self.f_spinbox.setValue(0)
        self.is_enabled.setChecked(False)
        self.__chg_enabled(QtCore.Qt.CheckState.Unchecked)

    def __chg_enabled(self, state: QtCore.Qt.CheckState):
        self.f_slider.setEnabled(bool(state))
        self.f_spinbox.setEnabled(bool(state))

    def setData(self, v: Optional[int] = None):
        if v is not None:
            self.f_spinbox.setValue(v)
            self.is_enabled.setChecked(True)
            self.__chg_enabled(QtCore.Qt.CheckState.Checked)
        else:
            self.__reset()

    def getData(self) -> Optional[int]:
        if self.is_enabled.isChecked():
            return self.f_spinbox.value()


class ProgressWidget(SlidedSpinBox):
    def __init__(self, parent=None):
        super().__init__(100, parent)
        self.f_slider.setMaximum(100)
        self.f_slider.valueChanged[int].connect(self.f_spinbox.setValue)
        self.f_spinbox.valueChanged[int].connect(self.f_slider.setValue)

    def setData(self, v: Optional[int] = None):
        super().setData(v)
        if v is not None:
            self.f_slider.setValue(v)


class PrioWidget(SlidedSpinBox):
    __spin2slide = (0, 5, 4, 4, 4, 3, 2, 2, 2, 1)
    __slide2spin = (0, 9, 7, 5, 3, 1)

    def __init__(self, parent=None):
        super().__init__(9, parent)
        self.f_spinbox.setReadOnly(True)
        self.f_slider.setMaximum(5)
        self.f_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.f_slider.setTickInterval(1)
        self.f_slider.valueChanged[int].connect(self._chg_slider)

    def _chg_slider(self, v: Optional[int] = None):
        self.f_spinbox.setValue(self.__slide2spin[v])

    def setData(self, v: Optional[int] = None):
        if v is not None:
            self.f_slider.setValue(self.__spin2slide[v])
        super().setData(v)  # avoid spinbox reset


class SpecialCombo(QtWidgets.QComboBox):
    _data2idx: dict[Any, int]
    _idx2data: tuple

    def __init__(self, items: tuple, parent=None):
        super().__init__(parent)
        self.addItems(items)

    def setData(self, v=None):
        if v is not None:
            self.setCurrentIndex(self._data2idx[v])

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
    :todo: Interim logic (on the fly, mandatory 'summary', .setValidator()
    :todo: popup/pulldown info: created, dtstamp, modified, sequence, uid
    :todo: select optional fields to show: class, ...
    :todo: set default values: priority, ...
    """
    f_store: QtWidgets.QComboBox
    f_category: QtWidgets.QLineEdit
    f_class: ClassCombo
    f_completed: CheckableDateTimeEdit
    f_description: QtWidgets.QPlainTextEdit
    f_dtstart: CheckableDateAndTimeEdit
    f_due: CheckableDateAndTimeEdit
    f_location: QtWidgets.QLineEdit
    f_progress: ProgressWidget  # Steps: TB/Evolution=1, Rainlendar=10, Reminder=x, OpenTodo=5
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
        self.f_store = StoreWidget(self)
        # attach[]
        self.f_category = QtWidgets.QLineEdit(self)  # TODO: checkable combobox
        self.f_class = ClassCombo(self)  # TODO: radio/slider?
        # comment[]
        self.f_completed = CheckableDateTimeEdit(self)
        # contact[]
        self.f_description = QtWidgets.QPlainTextEdit(self)
        self.f_dtstart = CheckableDateAndTimeEdit(self)
        self.f_due = CheckableDateAndTimeEdit(self)
        self.f_location = QtWidgets.QLineEdit(self)
        self.f_progress = ProgressWidget(self)
        self.f_priority = PrioWidget(self)
        # relatedto
        # rrule
        self.f_status = StatusCombo(self)  # TODO: radio?
        self.f_summary = QtWidgets.QLineEdit(self)
        self.f_url = QtWidgets.QLineEdit(self)
        self.f_category.setClearButtonEnabled(True)
        self.f_url.setClearButtonEnabled(True)
        self.f_location.setClearButtonEnabled(True)
        # the end
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def __setLayout(self):
        """Bests: Evolution, RTM"""
        layout = QtWidgets.QFormLayout(self)  # FIME: not h-stretchable
        layout.addRow("Store", self.f_store)
        layout.addRow("Summary", self.f_summary)
        layout.addRow("Category", self.f_category)
        layout.addRow("Class", self.f_class)  # on demand
        layout.addRow("Priority", self.f_priority)
        layout.addRow("DTStart", self.f_dtstart)  # on demand
        layout.addRow("Due", self.f_due)
        layout.addRow("Status", self.f_status)
        layout.addRow("% complete", self.f_progress)
        layout.addRow("Completed", self.f_completed)
        layout.addRow("Location", self.f_location)  # on demand
        layout.addRow("URL", self.f_url)  # on demand
        layout.addRow("Description", self.f_description)
        # the end
        layout.addRow(self.button_box)
        layout.setVerticalSpacing(0)
        self.setLayout(layout)

    def exec_new(self) -> Optional[tuple[TodoVObj, int]]:
        """Create new entry.
        :return: created obj and store_id
        """
        self.__reset()
        if self.exec_():
            obj = TodoVObj()
            if self.to_obj(obj):
                store = self.f_store.getData()
                return obj, store

    def exec_edit(self, vobj: TodoVObj, store: TodoStore) -> bool:
        """Edit entry exists.

        :param vobj: obj to edit
        :param store: source store
        :return: object was changed flag and [new] store_id.
        """
        self.from_obj(vobj, store)
        if self.exec_():
            return self.to_obj(vobj)
        return False

    def __reset(self):
        self.f_store.setEnabled(True)
        self.f_class.setData()
        self.f_completed.setData()
        self.f_description.clear()
        self.f_dtstart.setData()
        self.f_due.setData()
        self.f_location.clear()
        self.f_progress.setData()
        self.f_priority.setData()
        self.f_status.setData()
        self.f_summary.clear()
        self.f_url.clear()

    def from_obj(self, vobj: TodoVObj, store: TodoStore):
        """Preload form with VTODO"""
        self.f_store.setData(store)
        self.f_store.setEnabled(False)
        if v := vobj.get_Categories():
            self.f_category.setText(', '.join(v))
        self.f_class.setData(vobj.get_Class())
        self.f_completed.setData(v.astimezone() if (v := vobj.get_Completed()) else None)
        self.f_description.setPlainText(vobj.get_Description())
        self.f_dtstart.setData(vobj.get_DTStart())
        self.f_due.setData(vobj.get_Due())
        self.f_location.setText(vobj.get_Location())
        self.f_progress.setData(vobj.get_Progress())
        self.f_priority.setData(vobj.get_Priority())
        self.f_status.setData(vobj.get_Status())
        self.f_summary.setText(vobj.get_Summary())
        self.f_url.setText(vobj.get_URL())

    def to_obj(self, vobj: TodoVObj) -> bool:
        """Update VTodoObj from form.
        :param vobj: VTodoObj to update
        :return: True if vobj was changed
        """
        chgd = False
        # - cat
        if v_new := self.f_category.text():
            v_new = [s.strip() for s in v_new.split(',')]
            v_new.sort()
        else:  # empty list
            v_new = None
        chgd |= vobj.set_Categories(v_new)
        chgd |= vobj.set_Class(self.f_class.getData())
        if v_new := self.f_completed.getData():
            chgd |= vobj.set_Completed(v_new.astimezone(_tz_utc()))
        chgd |= vobj.set_Description(self.f_description.toPlainText() or None)
        chgd |= vobj.set_DTStart(self.f_dtstart.getData())
        chgd |= vobj.set_Due(self.f_due.getData())
        chgd |= vobj.set_Location(self.f_location.text() or None)
        chgd |= vobj.set_Progress(self.f_progress.getData())
        chgd |= vobj.set_Priority(self.f_priority.getData())
        chgd |= vobj.set_Status(self.f_status.getData())
        chgd |= vobj.set_Summary(self.f_summary.text() or None)
        chgd |= vobj.set_URL(self.f_url.text() or None)
        if chgd:
            vobj.updateStamps()
        return chgd
