"""GUI representation of ToDo things"""
# 1. std
import datetime
import os
from typing import Any
# 2. PySide
import vobject
from PySide2 import QtCore, QtWidgets
# 3. local
from common import EntryView, EntryListView, StoreListView, exc, MySettings, SetGroup
from .model import TodoStoreModel, TodoModel, TodoProxyModel, obj2rec
from .data import VObjTodo
from .form import TodoForm, form2rec_upd, form2obj
from . import enums


class TodoListView(EntryListView):
    _own_model = TodoProxyModel
    """List of todos"""
    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent, dependant)
        self._details.setModel(self.model().sourceModel())
        # addons
        self.loadCol2Show()
        self.setColumnHidden(self.model().sourceModel().fieldIndex('body'), True)
        self.loadColOrder()
        hh = self.horizontalHeader()
        hh.sectionMoved.connect(self.sectionMoved)
        hh.setSectionsMovable(True)
        for c in ('id', 'progress', 'priority', 'status'):
            hh.setSectionResizeMode(
                hh.visualIndex(self.model().sourceModel().fieldIndex(c)),
                hh.ResizeMode.ResizeToContents
            )
        # hh.setSectionResizeMode(hh.ResizeMode.ResizeToContents) - total
        self.sortByColumn(self.model().sourceModel().fieldIndex('id'))
        # signals
        # # self.activated.connect(self.rowChanged)
        self.selectionModel().currentRowChanged.connect(self.rowChanged)

    def rowChanged(self, idx):
        """:todo: find sourceModel row"""
        self._details.mapper.setCurrentModelIndex(
            self._details.mapper.model().index(self.model().mapToSource(idx).row(), 0)
        )

    def sectionMoved(self, _: int, __: int, ___: int):
        """Section lidx moved from ovidx to nvidx"""
        self.saveColOrder()

    def loadCol2Show(self):
        """[Re]load colums visibility from settings"""
        col2show = set(MySettings.get(SetGroup.ToDo, 'col2show'))
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
            realmodel = self.model().sourceModel()
            rec = realmodel.record()  # new empty
            obj2rec(obj, rec, store_id)
            if not realmodel.insertRecord(-1, rec):
                print("Something wrong with adding record")
            realmodel.select()  # FIXME: update the row only
            # adding obj to cache unavailable

    def entryEdit(self):
        idx = self.currentIndex()
        if not idx.isValid():
            return
        row = self.model().mapToSource(idx).row()
        realmodel: TodoModel = self.model().sourceModel()
        obj: VObjTodo = realmodel.getObj(row)
        rec = realmodel.record(row)
        store_id = rec.value('store_id')
        f = TodoForm(self)  # TODO: cache creation
        f.load(obj, store_id)    # model.relation(col).indexColumn()
        if f.exec_():
            if form2rec_upd(f, obj, rec):
                if not realmodel.setRecord(row, rec):
                    print("Something wrong with updating record")
                realmodel.setObj(rec, obj)
                realmodel.select()  # FIXME: update the record only

    def entryDel(self):
        idx = self.currentIndex()
        if not idx.isValid():
            return
        row = self.model().mapToSource(idx).row()
        realmodel: TodoModel = self.model().sourceModel()
        realmodel.delObj(row)
        if not realmodel.removeRow(row):
            print("Something wrong with deleting")
        realmodel.select()  # FIXME: update the record only

    def entryCat(self):
        """Show raw Entry content"""
        idx = self.selectionModel().currentIndex()
        if not idx.isValid():
            return
        realmodel = self.model().sourceModel()
        row = self.model().mapToSource(idx).row()
        rec = realmodel.record(row)
        body = rec.value('body')
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, "Entry content", rec.value('summary'))
        msg.setDetailedText(body)
        # msg.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        msg.exec_()

    def entryInside(self):
        """Show clean entry content
        :todo: style it
        Simple:
        msg.setText(raw['summary'])
        for ...
          txt += f"{k}: {v}\n"
        msg.setDetailedText(txt)
        """
        idx = self.selectionModel().currentIndex()
        if not idx.isValid():
            return
        realmodel = self.model().sourceModel()
        row = self.model().mapToSource(idx).row()
        raw = realmodel.getObj(row).RawContent()
        # icon, title, text
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.NoIcon, "Entry content", '')
        # richtext
        txt = "<html><body><table><tbody>"
        for k, v in raw.items():
            if k == 'description':
                v = f"<pre>{v}</pre>"
            txt += f"<tr><th>{k}:</th><td>{v}</td></tr>"
        txt += "<tbody></table></body><html>"
        msg.setText(txt)
        msg.setTextFormat(QtCore.Qt.RichText)
        # msg.setSizeGripEnabled(True)  # not works
        msg.exec_()


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
        syncStore(self._list.model().sourceModel(), rec.value('id'), rec.value('connection'))


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
        # text += __mk_row("Created", data.getCreated().isoformat())
        # text += __mk_row("DTSTamp", data.getDTStamp().isoformat())
        text += __mk_row("Modified", data.getLastModified().isoformat())
        text += __mk_row("Priority", data.getPriority())
        text += __mk_row("Categories", data.getCategories())
        text += __mk_row("Class", enums.Enum2Raw_Class.get(data.getClass()))
        # v = data.getDTStart()
        # print("Print DTSTart:", v, type(v))
        text += __mk_row("DTStart", v.isoformat() if (v := data.getDTStart()) else '---')
        text += __mk_row("Due", v.isoformat() if (v := data.getDue()) else '---')
        text += __mk_row("Progress", data.getPercent())
        text += __mk_row("Completed", v.isoformat() if (v := data.getCompleted()) else '---')
        text += __mk_row("Status", enums.Enum2Raw_Status.get(data.getStatus()))
        text += __mk_row("Location", data.getLocation())
        text += __mk_row("URL", data.getURL())
        if desc := data.getDescription():
            desc = '<br/>'.join(desc.splitlines())
        text += __mk_row("Description", desc)
        text += '</table>'
        self.details.setText(text)

    def setModel(self, model: TodoModel):
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
        self.stores.model().activeChanged.connect(self.list.model().sourceModel().updateFilterByStore)

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
                        if not model.insertRecord(-1, rec):
                            print(obj.getSummary(), "Something wrong with adding record")
                else:
                    raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")
    model.select()
