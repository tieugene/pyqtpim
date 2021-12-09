"""GUI representation of ToDo things"""
# 1. std
import datetime
import os
from typing import Any
# 2. PySide
import vobject
from PySide2 import QtCore, QtWidgets, QtSql
# 3. local
from common import EntryView, EntryListView, EntryListManagerView, exc
from .model import TodoListManagerModel, TodoListModel
from .data import Todo
from .form import TodoForm
from . import enums


class TodoListView(EntryListView):
    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent, dependant)
        self.setColumnHidden(self.model().fieldIndex('id'), True)
        self.setColumnHidden(self.model().fieldIndex('body'), True)

    def _empty_model(self) -> TodoListModel:
        return TodoListModel()

    def itemAdd(self):
        f = TodoForm(self)  # TODO: cache creation
        if f.exec_():
            size = self.model().rowCount()
            self.model().insertRow(size)
            item: Todo = self.model().item(size)
            if form2obj(f, item):   # ?
                item.save()

    def itemEdit(self):
        idx = self.selectionModel().currentIndex()
        if idx.isValid():
            i = idx.row()
            item: Todo = self.model().item(i)
            f = TodoForm(self)  # TODO: cache creation
            f.load(item)
            if f.exec_():
                if form2obj(f, item):
                    item.save()

    def itemDel(self):
        idx = self.selectionModel().currentIndex()
        if idx.isValid():
            self.model().removeRow(idx.row())


class TodoListManagerView(EntryListManagerView):
    _title = 'ToDo list'

    def __init__(self, parent, dependant: TodoListView):
        super().__init__(parent, dependant)

    def _empty_model(self) -> TodoListManagerModel:
        return TodoListManagerModel()

    def itemSync(self):
        """Sync Store with its connection"""
        if not (indexes := self.selectedIndexes()):
            return
        rec = self.model().record(indexes[0].row())
        syncStore(self._list.model(), rec.value('id'), rec.value('connection'))


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
        self.__fill_details(self.mapper.model().getEntry(idx))

    def __fill_details(self, data: Todo = None):    # TODO: clear on None
        def __mk_row(title: str, value: Any):
            if value is None:
                value = ''
            elif isinstance(value, list):
                value = '<ul><li>' + '</li><li>'.join(value) + '</li></ul>'
            elif isinstance(value, datetime.datetime):
                value = value.strftime('%y.%m.%d %H:%M')
            elif isinstance(value, datetime.date):
                value = value.strftime('%y.%m.%d')
            return f"<tr><th>{title}:</th><td>{value}</td></tr>"
        text = '<table>'
        text += __mk_row("Categories", data.getCategories())
        text += __mk_row("Class", enums.Enum2Raw_Class.get(data.getClass()))
        text += __mk_row("Completed", data.getCompleted())
        text += __mk_row("DTStart", data.getDTStart())
        text += __mk_row("Due", data.getDue())
        text += __mk_row("Location", data.getLocation())
        text += __mk_row("Percent", data.getPercent())
        text += __mk_row("Priority", data.getPriority())
        text += __mk_row("Priority", data.getPriority())
        text += __mk_row("Status", enums.Enum2Raw_Status.get(data.getStatus()))
        text += __mk_row("URL", data.getURL())
        if desc := data.getDescription():
            desc = '<br/>'.join(desc.splitlines())
        text += __mk_row("Description", desc)
        text += '</table>'
        self.details.setText(text)

    def setModel(self, model: QtSql.QSqlTableModel):
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

    :todo: unify and/or hide into Entry setX()
    """
    changed = False
    # - cat
    if v_new := src.f_category.text():
        v_new = [s.strip() for s in v_new.split(',')]
        v_new.sort()
    else:
        v_new = None
    v_old = dst.getCategories()
    if v_old != v_new:  # compare 0/1/2+ x 0/1/2+
        dst.setCategories(v_new)
        changed = True
    # - class (combo)
    v_new = src.f_class.getData()
    if dst.getClass() != v_new:
        dst.setClass(v_new)
        changed = True
    # - completed
    v_new = src.f_completed.getData()
    if dst.getCompleted() != v_new:
        dst.setCompleted(v_new)
        changed = True
    # - description
    v_new = src.f_description.toPlainText() or None
    if dst.getDescription() != v_new:
        dst.setDescription(v_new)
        changed = True
    # - dtstart
    v_new = src.f_dtstart.getData()
    if dst.getDTStart() != v_new:
        dst.setDTStart(v_new)
        changed = True
    # - due
    v_new = src.f_due.getData()
    if dst.getDue() != v_new:
        dst.setDue(v_new)
        changed = True
    # - location
    v_new = src.f_location.text() or None
    if dst.getLocation() != v_new:
        dst.setLocation(v_new)
        changed = True
    # - percent
    v_new = src.f_percent.getData()
    v_old = dst.getPercent()
    if v_old != v_new and not (v_new == 0 and v_old is None):   # FIXME: dirty hack
        dst.setPercent(v_new)
        changed = True
    # - priority
    v_new = src.f_priority.getData()
    v_old = dst.getPriority()
    if v_old != v_new and not (v_new == 0 and v_old is None):
        dst.setPriority(v_new)
        changed = True
    # - status (combo)
    v_new = src.f_status.getData()
    if dst.getStatus() != v_new:
        dst.setStatus(v_new)
        changed = True
    # - summary
    v_new = src.f_summary.text() or None
    if dst.getSummary() != v_new:
        dst.setSummary(v_new)
        changed = True
    # - url
    v_new = src.f_url.text() or None
    if dst.getURL() != v_new:
        dst.setURL(v_new)
        changed = True
    return changed


def syncStore(model: TodoListModel, store_id: int, path: str):
    """Sync VTODO records with file dir"""
    with os.scandir(path) as itr:
        for entry in itr:
            if not entry.is_file():
                continue
            with open(entry.path, 'rt') as stream:
                if ventry := vobject.readOne(stream):
                    if ventry.name == 'VCALENDAR' and 'vtodo' in ventry.contents:
                        vtodo = Todo(entry.path, ventry)
                        loadVtodo(model, store_id, vtodo)
                else:
                    raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")
    model.select()


def loadVtodo(model: TodoListModel, store_id: int, vtodo: Todo):
    """Load one VTODO file into DB

    :param model: destination.
    :param store_id: subj.
    :param vtodo: whole of iCalendar.
    :return:
    """
    rec = model.record()
    rec.setValue('store_id', store_id)
    rec.setValue('created', vtodo.getCreated().isoformat())
    rec.setValue('modified', vtodo.getLastModified().isoformat())
    rec.setValue('summary', vtodo.getSummary())
    rec.setValue('body', vtodo.serialize())
    if v := vtodo.getDTStart():
        rec.setValue('dtstart', v.isoformat())
    if v := vtodo.getDue():
        rec.setValue('due', v.isoformat())
    if v := vtodo.getCompleted():
        rec.setValue('completed', v.isoformat())
    if not (v := vtodo.getPercent()) is None:
        rec.setValue('progress', v)
    if not (v := vtodo.getPriority()) is None:
        rec.setValue('priority', v)
    if v := vtodo.getStatus():
        rec.setValue('status', v.value)
    if v := vtodo.getLocation():
        rec.setValue('location', v)
    ok = model.insertRecord(model.rowCount(), rec)
    if not ok:
        print(vtodo.summary, "Oops")
