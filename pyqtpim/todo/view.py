"""GUI representation of ToDo things"""
# 1. std
import datetime
from typing import Any
# 2. PySide
from PySide2 import QtCore, QtWidgets, QtSql
# 3. local
from common import EntryView, EntryListView, StoreListView, MySettings, SetGroup
from .model import TodoStoreModel, TodoModel, TodoProxyModel, obj2sql
from .data import TodoVObj
from .form import TodoForm
from . import enums


class TodoListView(EntryListView):
    _own_model = TodoProxyModel
    """List of todos"""
    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent, dependant)
        self._details.setModel(self.model().sourceModel())
        # addons
        self.loadCol2Show()
        self.setColumnHidden(enums.EColNo.Body.value, True)
        self.loadColOrder()
        hh = self.horizontalHeader()
        hh.sectionMoved.connect(self.sectionMoved)
        hh.setSectionsMovable(True)
        # vvv Works not right
        # for c in (enums.EColNo.ID.value, enums.EColNo.Progress.value, enums.EColNo.Prio.value,
        #           enums.EColNo.Status.value, enums.EColNo.Syn.value):
        #     hh.setSectionResizeMode(
        #         hh.visualIndex(c),
        #         hh.ResizeMode.ResizeToContents
        #     )
        # hh.setSectionResizeMode(hh.ResizeMode.ResizeToContents) - total
        self.sortByColumn(enums.EColNo.ID.value)
        # self.resizeRowsToContents()
        # signals
        # # self.activated.connect(self.rowChanged)
        self.selectionModel().currentRowChanged.connect(self.rowChanged)

    def requery(self):
        self.model().sourceModel().reload()
        self.resizeRowsToContents()

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
        if pair := f.exec_new():
            obj, store_id = pair
            # TODO: move to model
            q = obj2sql(query.entry_add, obj)
            q.bindValue(':store_id', store_id)
            q.bindValue(':syn', enums.ESyn.New.value)
            if not q.exec_():
                print(f"Something bad with adding record '{obj.get_Summary()}': {q.lastError().text()}")
            else:
                self.model().sourceModel().setObj(q.lastInsertId(), obj)
                self.requery()

    def entryEdit(self):
        idx = self.currentIndex()
        if not idx.isValid():
            return
        realmodel: TodoModel = self.model().sourceModel()
        row = self.model().mapToSource(idx).row()
        rec = realmodel.record(row)
        syn = rec.value('syn')
        if syn == enums.ESyn.Del.value:
            QtWidgets.QMessageBox.warning(self, "Edit deleted", "You cannot edit deleted entry")
            return
        entry_id = rec.value('id')
        store_id = rec.value('store_id')  # ??? returns model.data()
        # TODO: by id
        obj: TodoVObj = realmodel.getObjByRow(row)
        f = TodoForm(self)  # TODO: cache creation
        if pair := f.exec_edit(obj, store_id, can_move=(syn == enums.ESyn.New.value)):
            # TODO: move to model
            obj_chg, store_id_new = pair
            if obj_chg:  # FIXME: obj chg AND moved
                q = obj2sql(query.entry_upd, obj)
                q.bindValue(':store_id', store_id_new)
                q.bindValue(':id', entry_id)
                if not q.exec_():
                    print(f"Something bad with updating record '{obj.get_Summary()}': {q.lastError().text()}")
            else:  # just move to other store
                if not (q := QtSql.QSqlQuery(query.entry_mov % (store_id_new, entry_id))).exec_():
                    print(f"Something wrong with moving {entry_id}: {q.lastError().text()}")
            # realmodel.setObj(rec, obj)
            self.requery()  # FIXME: update the record only

    def entryDel(self):
        idx = self.currentIndex()
        if not idx.isValid():
            return
        src_row = self.model().mapToSource(idx).row()
        realmodel: TodoModel = self.model().sourceModel()
        # TODO: by id
        src_rec = realmodel.record(src_row)
        entry_id = src_rec.value('id')
        syn = src_rec.value('syn')
        # if not realmodel.removeRow(src_row):
        if QtWidgets.QMessageBox.question(self, f"Deleting {entry_id}",
                                          f"Are you sure to delete '{entry_id}'") \
                == QtWidgets.QMessageBox.StandardButton.Yes:
            # TODO: move to model
            if syn == enums.ESyn.New.value:
                if not (q := QtSql.QSqlQuery(query.entry_del % entry_id)).exec_():
                    print(f"Something wrong with deleting {entry_id}: {q.lastError().text()}")
                else:
                    realmodel.delObj(entry_id)
            elif syn == enums.ESyn.Synced.value:
                if not (q := QtSql.QSqlQuery(query.entry_set_syn % (enums.ESyn.Del.value, entry_id))).exec_():
                    print(f"Something wrong with mark deleted {entry_id}: {q.lastError().text()}")
            else:
                print(f"Entry already deleted: {entry_id}")
            self.requery()

    def entryCat(self):
        """Show raw Entry content"""
        idx = self.selectionModel().currentIndex()
        if not idx.isValid():
            return
        realmodel = self.model().sourceModel()
        # TODO: by id
        row = self.model().mapToSource(idx).row()
        # TODO: move to model
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
        # TODO: by id
        realmodel = self.model().sourceModel()
        row = self.model().mapToSource(idx).row()
        # TODO: move to model
        raw = realmodel.getObjByRow(row).RawContent()
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
    _model_cls = TodoStoreModel
    _title = 'ToDo list'

    def __init__(self, parent, dependant: TodoListView):
        super().__init__(parent, dependant)
        # self.model().activeChanged.connect(self._list.model().updateFilterByStore)

    def storeReload(self):
        """Reload Store from its connection"""
        if not (indexes := self.selectedIndexes()):
            return
        rec = self.model().record(indexes[0].row())
        self._list.model().sourceModel().reloadAll(rec.value('id'), rec.value('connection'))

    def storeSync(self, dry_run: bool = True):
        """Sync Store with its connection
        :todo: reset self._list.model().sourceModel(), reset its cache
        """
        if not (indexes := self.selectedIndexes()):
            return


class TodoView(EntryView):
    id_: QtWidgets.QSpinBox
    store: QtWidgets.QLineEdit
    summary: QtWidgets.QLineEdit
    category: QtWidgets.QLineEdit
    priority: QtWidgets.QLineEdit
    dtstart: QtWidgets.QLineEdit
    due: QtWidgets.QLineEdit
    status: QtWidgets.QLineEdit
    progress: QtWidgets.QLineEdit
    completed: QtWidgets.QLineEdit
    url: QtWidgets.QLineEdit
    location: QtWidgets.QLineEdit
    class_: QtWidgets.QLineEdit
    modified: QtWidgets.QDateTimeEdit
    description: QtWidgets.QTextEdit

    def __init__(self, parent):
        super().__init__(parent)
        self.__createWidgets()

    def __createWidgets(self):
        # widgets
        self.id_ = QtWidgets.QSpinBox(self)
        self.store = QtWidgets.QLineEdit(self)
        self.summary = QtWidgets.QLineEdit(self)
        self.category = QtWidgets.QLineEdit(self)
        self.priority = QtWidgets.QLineEdit(self)
        self.dtstart = QtWidgets.QLineEdit(self)
        self.due = QtWidgets.QLineEdit(self)
        self.status = QtWidgets.QLineEdit(self)
        self.progress = QtWidgets.QLineEdit(self)
        self.completed = QtWidgets.QLineEdit(self)
        self.url = QtWidgets.QLineEdit(self)
        self.location = QtWidgets.QLineEdit(self)
        self.class_ = QtWidgets.QLineEdit(self)
        self.modified = QtWidgets.QDateTimeEdit(self)
        self.description = QtWidgets.QTextEdit(self)
        # attributes
        for i in (self.id_, self.store, self.summary, self.category, self.priority, self.dtstart, self.due, self.status,
                  self.progress, self.completed, self.url, self.location, self.class_, self.modified, self.description):
            i.setReadOnly(True)
        for i in (self.id_, self.modified):
            i.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.id_.setMaximum(1 << 30)
        # layout
        layout = QtWidgets.QFormLayout()
        layout.addRow("ID", self.id_)
        layout.addRow("Store", self.store)
        layout.addRow("Summary:", self.summary)
        layout.addRow("Category:", self.category)
        layout.addRow("Priority:", self.priority)
        layout.addRow("DTStart:", self.dtstart)
        layout.addRow("Due:", self.due)
        layout.addRow("Status:", self.status)
        layout.addRow("Progress:", self.progress)
        layout.addRow("Completed:", self.completed)
        layout.addRow("URL:", self.url)
        layout.addRow("Location:", self.location)
        layout.addRow("Class:", self.class_)
        layout.addRow("Modified:", self.modified)
        layout.addRow(self.description)
        layout.setVerticalSpacing(0)    # default=-1
        self.setLayout(layout)
        # print("vSpace:", layout.verticalSpacing())
        # print("hSpace:", layout.horizontalSpacing())

    def __idxChgd(self, row: int):
        """Only for selection; not calling on deselection"""
        # FIXME: clean prio, progress, completed
        data = self.mapper.model().getObjByRow(row)
        self.category.setText(', '.join(v) if (v := data.get_Categories()) else None)
        self.url.setText(data.get_URL())
        self.class_.setText(enums.Enum2Raw_Class.get(data.get_Class()))
        self.description.setText(data.get_Description())

    def setModel(self, model: TodoModel):
        """Setup mapper
        :todo: indexOf
        """
        super().setModel(model)
        self.mapper.addMapping(self.id_, enums.EColNo.ID.value)
        self.mapper.addMapping(self.store, enums.EColNo.Store.value)
        self.mapper.addMapping(self.summary, enums.EColNo.Summary.value)
        # category
        self.mapper.addMapping(self.priority, enums.EColNo.Prio.value)
        self.mapper.addMapping(self.dtstart, enums.EColNo.DTStart.value)
        self.mapper.addMapping(self.due, enums.EColNo.Due.value)
        self.mapper.addMapping(self.status, enums.EColNo.Status.value)
        self.mapper.addMapping(self.progress, enums.EColNo.Progress.value)
        self.mapper.addMapping(self.completed, enums.EColNo.Completed.value)
        # URL
        self.mapper.addMapping(self.location, enums.EColNo.Location.value)
        # class
        self.mapper.addMapping(self.modified, enums.EColNo.Modified.value)
        # description
        self.mapper.currentIndexChanged.connect(self.__idxChgd)


class TodoSortWidget(QtWidgets.QGroupBox):
    by_id: QtWidgets.QRadioButton
    by_name: QtWidgets.QRadioButton
    by_pdn: QtWidgets.QRadioButton
    bg: QtWidgets.QButtonGroup

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Sort")
        # widgets
        self.by_id = QtWidgets.QRadioButton("ID", self)
        self.by_name = QtWidgets.QRadioButton("Name", self)
        self.by_pdn = QtWidgets.QRadioButton("!→Due→Name", self)
        # logic
        self.bg = QtWidgets.QButtonGroup(self)
        self.bg.addButton(self.by_id, enums.ESortBy.ID)
        self.bg.addButton(self.by_name, enums.ESortBy.Name)
        self.bg.addButton(self.by_pdn, enums.ESortBy.PrioDueName)
        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.by_id)
        layout.addWidget(self.by_name)
        layout.addWidget(self.by_pdn)
        # layout.addStretch(1);
        self.setLayout(layout)
        # the end
        self.by_id.setChecked(True)


class TodoFilterWidget(QtWidgets.QGroupBox):
    f_All: QtWidgets.QRadioButton
    f_Closed: QtWidgets.QRadioButton
    f_Today: QtWidgets.QRadioButton
    f_Tomorrow: QtWidgets.QRadioButton
    bg: QtWidgets.QButtonGroup

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Filter")
        # widgets
        self.f_All = QtWidgets.QRadioButton("All", self)
        self.f_Closed = QtWidgets.QRadioButton("Closed", self)
        self.f_Today = QtWidgets.QRadioButton("Today", self)
        self.f_Tomorrow = QtWidgets.QRadioButton("Tomorrow", self)
        # logic
        self.bg = QtWidgets.QButtonGroup(self)
        self.bg.addButton(self.f_All, enums.EFiltBy.All)
        self.bg.addButton(self.f_Closed, enums.EFiltBy.Closed)
        self.bg.addButton(self.f_Today, enums.EFiltBy.Today)
        self.bg.addButton(self.f_Tomorrow, enums.EFiltBy.Tomorrow)
        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.f_All)
        layout.addWidget(self.f_Closed)
        layout.addWidget(self.f_Today)
        layout.addWidget(self.f_Tomorrow)
        # layout.addStretch(1);
        self.setLayout(layout)
        # the end
        self.f_All.setChecked(True)


class TodosWidget(QtWidgets.QWidget):
    stores: TodoStoreListView
    l_sort: TodoSortWidget
    l_filt: TodoFilterWidget
    # l_filt: QtWidgets.QGroupBox
    list: TodoListView
    details: TodoView

    def __init__(self):
        super().__init__()
        self.__createWidgets()
        self.__createConnections()

    def __createWidgets(self):
        # order
        splitter = QtWidgets.QSplitter(self)
        self.details = TodoView(splitter)
        self.list = TodoListView(splitter, self.details)
        left_panel = QtWidgets.QWidget(splitter)
        self.stores = TodoStoreListView(left_panel, self.list)
        self.l_sort = TodoSortWidget(left_panel)
        self.l_filt = TodoFilterWidget(left_panel)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.addWidget(self.stores)
        left_layout.addWidget(self.l_sort)
        left_layout.addWidget(self.l_filt)
        left_panel.setLayout(left_layout)
        # layout
        splitter.addWidget(left_panel)
        splitter.addWidget(self.list)
        splitter.addWidget(self.details)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(splitter)
        self.setLayout(layout)

    def __createConnections(self):
        self.stores.model().activeChanged.connect(self.list.model().sourceModel().updateFilterByStore)
        self.l_sort.bg.idClicked.connect(self.list.model().sortChanged)
        self.l_filt.bg.idClicked.connect(self.list.model().filtChanged)
