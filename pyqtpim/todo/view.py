"""GUI representation of ToDo things"""
# 1. std
import datetime
import os
from typing import Any
# 2. PySide
import vobject
from PySide2 import QtCore, QtWidgets, QtSql
# 3. local
from common import EntryView, EntryListView, StoreListView, exc, MySettings, SetGroup
from .model import TodoStoreModel, TodoModel, obj2rec
from .data import VObjTodo
from .form import TodoForm, form2rec_upd, form2obj
from . import enums


class TodoListView(EntryListView):
    _own_model = TodoModel
    """List of todos"""
    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent, dependant)
        self.reloadCol2Show()
        self.setColumnHidden(self.model().fieldIndex('body'), True)
        self.loadColOrder()
        self.horizontalHeader().sectionMoved.connect(self.sectionMoved)
        self.horizontalHeader().setSectionsMovable(True)
        self.sortByColumn(self.model().fieldIndex('id'))

    def sectionMoved(self, lidx: int, ovidx: int, nvidx: int):
        """Section lidx moved from ovidx to nvidx"""
        self.saveColOrder()

    def reloadCol2Show(self):
        """[Re]load colums visibility from settings"""
        col2show = MySettings.get(SetGroup.ToDo, 'col2show')
        for i in range(self.model().columnCount()):
            self.setColumnHidden(i, not (i in col2show))

    def loadColOrder(self):
        """[Re]load columns order from settings"""
        col_order = MySettings.get(SetGroup.ToDo, 'colorder')
        for vi, li in enumerate(col_order):
            if (cvi := self.horizontalHeader().visualIndex(li)) != vi:
                self.horizontalHeader().moveSection(cvi, vi)

    def saveColOrder(self):
        """[Re]save columns order to settings"""
        col_order = list()
        for vi in range(self.horizontalHeader().count()):
            col_order.append(self.horizontalHeader().logicalIndex(vi))  # colorder[vi] = li
        MySettings.set(SetGroup.ToDo, 'colorder', col_order)

    def entryAdd(self):
        f = TodoForm(self)  # TODO: cache creation
        if f.exec_():
            obj, store_id = form2obj(f)
            rec = self.model().record()  # new empty
            obj2rec(obj, rec, store_id)
            self.model().insertRecord(-1, rec)
            self.model().select()
            # adding obj to cache unavailable

    def entryEdit(self):
        idx = self.currentIndex()
        if idx.isValid():
            row = idx.row()
            model: TodoModel = self.model()
            obj: VObjTodo = model.getObj(row)
            rec = model.record(row)
            store_id = rec.value('store_id')
            f = TodoForm(self)  # TODO: cache creation
            f.load(obj, store_id)    # model.relation(col).indexColumn()
            if f.exec_():
                if form2rec_upd(f, obj, rec):
                    model.setRecord(row, rec)
                    model.setObj(rec, obj)

    def entryDel(self):
        idx = self.currentIndex()
        if idx.isValid():
            row = idx.row()
            model: TodoModel = self.model()
            model.delObj(row)
            model.removeRow(row)
            model.select()


class TodoStoreListView(StoreListView):
    _own_model = TodoStoreModel
    _title = 'ToDo list'

    def __init__(self, parent, dependant: TodoListView):
        super().__init__(parent, dependant)
        # self.model().activeChanged.connect(self._list.model().updateFilterByStore)

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

    def __idxChgd(self, row: int):
        """Only for selection; not calling on deselection"""
        self.__fill_details(self.mapper.model().getObj(row))

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
    stores: TodoStoreListView
    list: TodoListView
    details: TodoView

    def __init__(self):
        super().__init__()
        self.__createWidgets()
        self.stores.model().activeChanged.connect(self.list.model().updateFilterByStore)

    def __createWidgets(self):
        # order
        splitter = QtWidgets.QSplitter(self)
        self.details = TodoView(splitter)
        self.list = TodoListView(splitter, self.details)
        self.stores = TodoStoreListView(splitter, self.list)
        # layout
        splitter.addWidget(self.stores)
        splitter.addWidget(self.list)
        splitter.addWidget(self.details)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(splitter)
        self.setLayout(layout)


def syncStore(model: TodoModel, store_id: int, path: str):
    """Sync VTODO records with file dir
    :todo: hide into model
    """
    with os.scandir(path) as itr:
        for entry in itr:
            if not entry.is_file():
                continue
            with open(entry.path, 'rt') as stream:
                if ventry := vobject.readOne(stream):
                    if ventry.name == 'VCALENDAR' and 'vtodo' in ventry.contents:
                        obj = VObjTodo(ventry)
                        rec = model.record()
                        obj2rec(obj, rec, store_id)
                        # rec.setValue('store_id', store_id)
                        ok = model.insertRecord(-1, rec)
                        if not ok:
                            print(obj.getSummary(), "Oops")
                else:
                    raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")
    model.select()
