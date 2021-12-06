"""GUI representation of ToDo things"""
# 1. std
import datetime
from typing import Any
# 2. PySide
from PySide2 import QtCore, QtWidgets
# 3. local
from common import EntryView, EntryListView, EntryListManagerView
from .model import TodoListManagerModel, TodoListModel
from .data import Todo
from .form import TodoForm
from . import enums


class TodoListManagerView(EntryListManagerView):
    _title = 'ToDo list'

    def _empty_model(self) -> TodoListManagerModel:
        return TodoListManagerModel()


class TodoListView(EntryListView):
    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent, dependant)
        # self.setColumnHidden(1, True)

    def _empty_model(self) -> TodoListModel:
        return TodoListModel()

    def itemAdd(self):
        f = TodoForm(self)  # TODO: cache creation
        f.exec_()

    def itemEdit(self):
        idx = self.selectionModel().currentIndex()
        if idx.isValid():
            i = idx.row()
            item: Todo = self.model().item(i)
            f = TodoForm(self)  # TODO: cache creation
            f.load(item)
            if f.exec_():
                if form2obj(f, item):
                    print("Wanna be saved:")
                    print(item.serialize())
            # print("Edit", item.getSummary())

    def itemDel(self):
        idx = self.selectionModel().currentIndex()
        if idx.isValid():
            i = idx.row()
            item: Todo = self.model().item(i)
            print("Del", item.getSummary())


class TodoView(EntryView):
    summary: QtWidgets.QLineEdit
    details: QtWidgets.QTextEdit

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Details")
        self.__createWidgets()

    def __createWidgets(self):
        # widgets
        self.summary = QtWidgets.QLineEdit(self)
        self.details = QtWidgets.QTextEdit(self)
        # attributes
        self.summary.setReadOnly(True)
        self.details.setReadOnly(True)
        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.summary)
        layout.addWidget(self.details)
        self.setLayout(layout)

    def __idxChgd(self, idx: int):
        """Only for selection; not calling on deselection"""
        self.__fill_details(self.mapper.model().item(idx))

    def __fill_details(self, data: Todo = None):    # TODO: clear on None
        __DemapStatus = {
            enums.EStatus.NeedsAction: "Do something",
            enums.EStatus.InProcess: "wait...",
            enums.EStatus.Completed: "OK",
            enums.EStatus.Cancelled: "WontFix",
        }

        def __mk_row(title: str, value: Any):
            if isinstance(value, list):
                value = '<ul><li>' + '</li><li>'.join(value) + '</li></ul>'
            elif isinstance(value, datetime.datetime):
                value = value.strftime('%y.%m.%d %H:%M')
            elif isinstance(value, datetime.date):
                value = value.strftime('%y.%m.%d')
            return f"<tr><th>{title}:</th><td>{value}</td></tr>"
        text = '<table>'
        if v := data.getCategories():
            text += __mk_row("Categories", v)
        if v := data.getCompleted():
            text += __mk_row("Completed", v)
        if v := data.getDTStart():
            text += __mk_row("DTStart", v)
        if v := data.getDue():
            text += __mk_row("Due", v)
        if v := data.getLocation():
            text += __mk_row("Location", v)
        if v := data.getPercent():
            text += __mk_row("Percent", v)
        if v := data.getPriority():
            text += __mk_row("Priority", v)
        if v := data.getStatus():
            text += __mk_row("Status", __DemapStatus[v])
        text += '</table>'
        self.details.setText(text)

    def setModel(self, model: QtCore.QStringListModel):
        """Setup mapper
        :todo: indexOf
        """
        super().setModel(model)
        self.mapper.addMapping(self.summary, 0)
        self.mapper.currentIndexChanged.connect(self.__idxChgd)

    def clean(self):
        self.summary.clear()
        self.details.clear()


class TodosWidget(QtWidgets.QWidget):
    sources: TodoListManagerView
    list: TodoListView
    details: TodoView

    def __init__(self):
        super().__init__()
        self.__createWidgets()

    def __createWidgets(self):
        # order
        splitter = QtWidgets.QSplitter(self)
        self.details = TodoView(splitter)
        self.list = TodoListView(splitter, self.details)
        self.sources = TodoListManagerView(splitter, self.list)
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


def form2obj(src: TodoForm, dst: Todo) -> bool:
    """Update Todo entry with form values.
    :return: True if anythong changed and entry must be saved.
    """
    def __prn_chg(title: str, old: Any, new: Any):
        print(title, " chg:", old, "=>", new)
    changed = False
    # - cat
    if v_new := src.f_category.text():
        v_new = [s.strip() for s in v_new.split(',')]
        v_new.sort()
        if len(v_new) == 1:
            v_new = v_new[0]
    else:
        v_new = None
    v_old = dst.getCategories()
    if v_old != v_new:  # compare 0/1/2+ x 0/1/2+
        changed = True
        __prn_chg("Categories", v_old, v_new)
    # - class (combo)
    v_new = src.f_class.getData()
    v_old = dst.getClass()
    if v_old != v_new:
        changed = True
        __prn_chg("Class", v_old, v_new)
    # - completed
    v_new = src.f_completed.getData()
    v_old = dst.getCompleted()
    if v_old != v_new:
        changed = True
        __prn_chg("Completed", v_old, v_new)
    # - description
    v_new = src.f_description.toPlainText() or None
    v_old = dst.getDescription()
    if v_old != v_new:
        changed = True
        __prn_chg("Desc", v_old, v_new)
    # - dtstart
    v_new = src.f_dtstart.getData()
    v_old = dst.getDTStart()
    if v_old != v_new:
        changed = True
        __prn_chg("DTStart", v_old, v_new)
    # - due
    v_new = src.f_due.getData()
    v_old = dst.getDue()
    if v_old != v_new:
        changed = True
        __prn_chg("Due", v_old, v_new)
    # - location
    v_new = src.f_location.text() or None
    v_old = dst.getLocation()
    if v_old != v_new:
        changed = True
        __prn_chg("Loc", v_old, v_new)
    # - percent
    v_new = src.f_percent.getData()
    v_old = dst.getPercent()
    if v_old != v_new and not (v_new == 0 and v_old is None):   # FIXME: dirty hack
        changed = True
        __prn_chg("%", v_old, v_new)
    # - priority
    v_new = src.f_priority.getData()
    v_old = dst.getPriority()
    if v_old != v_new:
        changed = True
        __prn_chg("Prio", v_old, v_new)
    # - status (combo)
    v_new = src.f_status.getData()
    v_old = dst.getStatus()
    if v_old != v_new:
        changed = True
        __prn_chg("Status", v_old, v_new)
    # - summary
    v_new = src.f_summary.text() or None
    v_old = dst.getSummary()
    if v_old != v_new:
        changed = True
        __prn_chg("Summary", v_old, v_new)
    # - url
    v_new = src.f_url.text() or None
    v_old = dst.getURL()
    if v_old != v_new:
        __prn_chg("URL", v_old, v_new)
        dst.setURL(v_new)
        changed = True
    return changed
