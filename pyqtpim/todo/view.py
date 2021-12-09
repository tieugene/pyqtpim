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
from .data import VObjTodo
from .form import TodoForm, form2rec_upd
from . import enums


class TodoListView(EntryListView):
    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent, dependant)
        self.setColumnHidden(self.model().fieldIndex('id'), True)
        self.setColumnHidden(self.model().fieldIndex('body'), True)

    def _empty_model(self) -> TodoListModel:
        return TodoListModel()

    def entryAdd(self):
        f = TodoForm(self)  # TODO: cache creation
        if f.exec_():
            size = self.model().rowCount()
            self.model().insertRow(size)
            entry: VObjTodo = self.model().item(size)
            if form2rec_upd(f, entry):   # ?
                # FIXME:
                entry.save()

    def entryEdit(self):
        idx = self.currentIndex()
        if idx.isValid():
            row = idx.row()
            model: TodoListModel = self.model()
            entry: VObjTodo = model.getEntry(row)
            rec = model.record(row)
            store_id = rec.value('store_id')
            f = TodoForm(self)  # TODO: cache creation
            f.load(entry, store_id)    # model.relation(col).indexColumn()
            if f.exec_():
                if form2rec_upd(f, entry, rec):
                    model.setRecord(row, rec)

    def entryDel(self):
        idx = self.currentIndex()
        if idx.isValid():
            self.model().removeRow(idx.row())


class TodoListManagerView(EntryListManagerView):
    _title = 'ToDo list'

    def __init__(self, parent, dependant: TodoListView):
        super().__init__(parent, dependant)

    def _empty_model(self) -> TodoListManagerModel:
        return TodoListManagerModel()

    def storeSync(self):
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

    def __fill_details(self, data: VObjTodo = None):    # TODO: clear on None
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
        self.mapper.addMapping(self.summary, model.fieldIndex('summary'))
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


def syncStore(model: TodoListModel, store_id: int, path: str):
    """Sync VTODO records with file dir"""
    with os.scandir(path) as itr:
        for entry in itr:
            if not entry.is_file():
                continue
            with open(entry.path, 'rt') as stream:
                if ventry := vobject.readOne(stream):
                    if ventry.name == 'VCALENDAR' and 'vtodo' in ventry.contents:
                        vtodo = VObjTodo(ventry)
                        rec = obj2rec(vtodo)   # FIXME: updateRecord()
                        rec.setValue('store_id', store_id)
                        ok = model.insertRecord(model.rowCount(), rec)  # or -1
                        if not ok:
                            print(vtodo.getSummary(), "Oops")
                else:
                    raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")
    model.select()
