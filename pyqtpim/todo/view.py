"""GUI representation of Tasks things"""
# 1. std
# 2. PySide
from PySide2 import QtCore, QtWidgets
# 3. local
from pym_core.todo.data import TodoVObj, TodoEntry
from pym_core.todo import enums as core_enums
from base import EntryView, EntryListView, StoreListView, MySettings, SetGroup
from .model import TodoStoreModel, TodoModel, TodoProxyModel, todo_model, store_model
from .form import TodoForm
from . import enums


class TodoListView(EntryListView):
    # _own_model = TodoProxyModel
    """List of todos"""

    def __init__(self, parent, dependant: EntryView):
        super().__init__(parent, dependant)
        # models
        proxy = TodoProxyModel(self)
        proxy.setSourceModel(todo_model)
        self.setModel(proxy)
        self._details.setModel(self.model().sourceModel())
        # misc
        self.loadCol2Show()
        self.__loadColOrder()
        hh = self.horizontalHeader()
        hh.setSectionsMovable(True)
        # vvv Works not right
        for c in (enums.EColNo.Prio, enums.EColNo.Status, enums.EColNo.Progress, enums.EColNo.Due):
            hh.setSectionResizeMode(c.value, hh.ResizeMode.ResizeToContents)
            # hh.setSectionResizeMode(hh.visualIndex(c), hh.ResizeMode.ResizeToContents)
        # hh.setSectionResizeMode(hh.ResizeMode.ResizeToContents) - total
        self.setSortingEnabled(True)  # deafult=False, requires sorting itself; must be NOT in parent
        self.verticalHeader().setSectionResizeMode(self.verticalHeader().ResizeMode.ResizeToContents)
        self.__form = TodoForm(self)
        # signals
        self.horizontalHeader().sectionMoved.connect(self.__sectionMoved)
        self.selectionModel().currentRowChanged.connect(self.__rowChanged)

    def __rowChanged(self, dst: QtCore.QModelIndex, src: QtCore.QModelIndex):
        if not dst.isValid():
            if src.isValid():
                self._details.clear()
                self.actionsChange.emit(False)
                # TODO: switch actions off
        else:
            self._details.mapper.setCurrentModelIndex(
                self._details.mapper.model().index(self.model().mapToSource(dst).row(), 0)
            )
            if not src.isValid():
                # TODO: switch actions on
                self.actionsChange.emit(True)

    def __sectionMoved(self, _: int, __: int, ___: int):
        """Section lidx moved from ovidx to nvidx"""
        self.__saveColOrder()

    def __saveColOrder(self):
        """[Re]save columns order to settings"""
        col_order = list()
        for vi in range(self.horizontalHeader().count()):
            col_order.append(self.horizontalHeader().logicalIndex(vi))  # colorder[vi] = li
        MySettings.set(SetGroup.ToDo, 'colorder', col_order)

    def loadCol2Show(self):
        """[Re]load colums visibility from settings"""
        col2show = set(MySettings.get(SetGroup.ToDo, 'col2show'))
        for i in range(self.model().columnCount()):
            self.setColumnHidden(i, not (i in col2show))

    def __loadColOrder(self):
        """[Re]load columns order from settings"""
        col_order = MySettings.get(SetGroup.ToDo, 'colorder')
        for vi, li in enumerate(col_order):
            if (cvi := self.horizontalHeader().visualIndex(li)) != vi:
                self.horizontalHeader().moveSection(cvi, vi)

    def entryAdd(self):
        if pair := self.__form.exec_new():
            vobj, store = pair
            fname = vobj.get_UID() + '.ics'
            entry = TodoEntry(vobj, store, fname)
            if entry.save():
                if not self.model().sourceModel().item_add(entry):
                    print(f"Something bad with adding '{vobj.get_Summary()}'")
            else:
                print(f"Error saving '{vobj.get_Summary()}'")

    def entryEdit(self):
        idx = self.currentIndex()
        if not idx.isValid():
            return
        row = self.model().mapToSource(idx).row()
        realmodel: TodoModel = self.model().sourceModel()
        entry = realmodel.item_get(row)
        if self.__form.exec_edit(entry.vobj, entry.store):
            if not realmodel.item_upd(row):
                print(f"Something bad with saving '{entry.vobj.get_Summary()}'")
            self.model().resortfilter()
            self.__rowChanged(self.currentIndex(), self.currentIndex())

    def entryDel(self):
        idx = self.currentIndex()
        if not idx.isValid():
            return
        row = self.model().mapToSource(idx).row()
        realmodel: TodoModel = self.model().sourceModel()
        name = realmodel.item_get(row).vobj.get_Summary()
        if QtWidgets.QMessageBox.question(self, "Deleting ToDo",
                                          f"Are you sure to delete '{name}'") \
                == QtWidgets.QMessageBox.StandardButton.Yes:
            if not realmodel.item_del(row):
                print(f"Something wrong with deleting '{name}'")
            self.model().resortfilter()

    def entryCat(self):
        """Show raw Entry content
        :todo: expandable text window"""
        idx = self.selectionModel().currentIndex()
        if not idx.isValid():
            return
        vobj = self.model().sourceModel().item_get(self.model().mapToSource(idx).row()).vobj
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, "Entry content", vobj.get_Summary())
        msg.setDetailedText(vobj.serialize())
        # msg.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        msg.exec_()

    def entryInside(self):
        """Show clean entry content
        :todo: style it
        """
        idx = self.selectionModel().currentIndex()
        if not idx.isValid():
            return
        vobj = self.model().sourceModel().item_get(self.model().mapToSource(idx).row()).vobj
        # icon, title, text
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.NoIcon, "Entry content", vobj.get_Summary())
        # richtext
        txt = "<html><body><table><tbody>"
        for k, v in vobj.RawContent().items():
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
    _title = 'ToDo Store'

    def __init__(self, parent, dependant: TodoListView):
        super().__init__(parent, dependant)
        self.setModel(store_model)
        # after setModel() only
        self.selectionModel().currentRowChanged.connect(self.__rowChanged)

    def __rowChanged(self, dst: QtCore.QModelIndex, src: QtCore.QModelIndex):
        dst_ok = dst.isValid()
        src_ok = src.isValid()
        if not dst_ok and src_ok:
            # TODO: switch action off
            self.actionsChange.emit(False)
        elif dst_ok and not src_ok:
            # TODO: switch action on
            self.actionsChange.emit(True)

    def stores_reload(self):
        """Reload Store from its connection"""
        # if not (indexes := self.selectedIndexes()):
        #    return
        self.model().load_self()
        self.model().load_entries()


class TodoView(EntryView):
    store: QtWidgets.QLineEdit
    summary: QtWidgets.QLineEdit
    category: QtWidgets.QLineEdit
    priority: QtWidgets.QLineEdit
    dtstart: QtWidgets.QLineEdit
    due: QtWidgets.QLineEdit
    status: QtWidgets.QLineEdit
    progress: QtWidgets.QLineEdit
    completed: QtWidgets.QLineEdit
    location: QtWidgets.QLineEdit
    class_: QtWidgets.QLineEdit
    url: QtWidgets.QLineEdit
    # url: QtWidgets.QLabel
    description: QtWidgets.QTextEdit
    created: QtWidgets.QLineEdit
    dtstamp: QtWidgets.QLineEdit
    modified: QtWidgets.QLineEdit
    # misc
    tabs: QtWidgets.QTabWidget
    tab_main: QtWidgets.QWidget
    tab_desc: QtWidgets.QWidget
    tab_misc: QtWidgets.QWidget

    def __init__(self, parent):
        super().__init__(parent)
        self.__createWidgets()

    def __createWidgets(self):
        # widgets
        self.store = QtWidgets.QLineEdit(self)
        self.summary = QtWidgets.QLineEdit(self)
        self.category = QtWidgets.QLineEdit(self)
        self.priority = QtWidgets.QLineEdit(self)
        self.dtstart = QtWidgets.QLineEdit(self)
        self.due = QtWidgets.QLineEdit(self)
        self.status = QtWidgets.QLineEdit(self)
        self.progress = QtWidgets.QLineEdit(self)
        self.completed = QtWidgets.QLineEdit(self)
        self.location = QtWidgets.QLineEdit(self)
        self.class_ = QtWidgets.QLineEdit(self)
        self.url = QtWidgets.QLineEdit(self)
        # self.url = QtWidgets.QLabel(self)
        self.description = QtWidgets.QTextEdit(self)
        self.created = QtWidgets.QLineEdit(self)
        self.dtstamp = QtWidgets.QLineEdit(self)
        self.modified = QtWidgets.QLineEdit(self)
        # tabs
        self.tabs = QtWidgets.QTabWidget(self)
        self.tab_main = QtWidgets.QWidget(self)
        self.tabs.addTab(self.tab_main, "Main")
        self.tab_desc = QtWidgets.QWidget(self)
        self.tabs.addTab(self.tab_desc, "Desc")
        self.tab_misc = QtWidgets.QWidget(self)
        self.tabs.addTab(self.tab_misc, "Misc")
        # attributes
        for i in (self.store, self.summary, self.category, self.priority, self.dtstart, self.due, self.status,
                  self.progress, self.completed, self.location, self.class_, self.url, self.description,
                  self.created, self.dtstamp, self.modified):
            i.setReadOnly(True)
        # self.url.setTextFormat(QtCore.Qt.RichText)
        # self.url.setWordWrap(True)
        # layouts
        # - 1
        layout_main = QtWidgets.QFormLayout()
        layout_main.addRow("Store", self.store)
        layout_main.addRow("Summary:", self.summary)
        layout_main.addRow("Category:", self.category)
        layout_main.addRow("Priority:", self.priority)
        layout_main.addRow("DTStart:", self.dtstart)
        layout_main.addRow("Due:", self.due)
        layout_main.addRow("Status:", self.status)
        layout_main.addRow("Progress:", self.progress)
        layout_main.addRow("Completed:", self.completed)
        layout_main.addRow("Location:", self.location)
        layout_main.addRow("Class:", self.class_)
        layout_main.addRow("URL:", self.url)
        # layout.addRow(self.description)
        layout_main.setVerticalSpacing(0)  # default=-1
        self.tab_main.setLayout(layout_main)
        # - 2
        layout_desc = QtWidgets.QVBoxLayout()
        layout_desc.addWidget(self.description)
        self.tab_desc.setLayout(layout_desc)
        # - 3
        layout_misc = QtWidgets.QFormLayout()
        layout_misc.addRow("Created:", self.created)
        layout_misc.addRow("DTStamp:", self.dtstamp)
        layout_misc.addRow("Modified:", self.modified)
        layout_misc.setVerticalSpacing(0)  # default=-1
        self.tab_misc.setLayout(layout_misc)
        # print("vSpace:", layout.verticalSpacing())
        # print("hSpace:", layout.horizontalSpacing())

    def __idxChgd(self, row: int):
        """Only for selection; not calling on deselection"""
        # FIXME: clean prio, progress, completed
        data: TodoVObj = self.mapper.model().item_get(row).vobj
        self.category.setText(', '.join(v) if (v := data.get_Categories()) else None)
        self.class_.setText(core_enums.Enum2Raw_Class.get(data.get_Class()))
        self.url.setText(data.get_URL())
        # if v := data.get_URL():
        #    self.url.setText(f"<a href=\"v\">{v}</a>")
        # else:
        #    self.url.clear()
        self.description.setText(data.get_Description())

    def setModel(self, model: TodoModel):
        """Setup mapper
        :todo: indexOf
        """
        super().setModel(model)
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
        self.mapper.addMapping(self.created, enums.EColNo.Created.value)
        self.mapper.addMapping(self.dtstamp, enums.EColNo.DTStamp.value)
        self.mapper.addMapping(self.modified, enums.EColNo.Modified.value)
        # description
        self.mapper.currentIndexChanged.connect(self.__idxChgd)

    def clear(self):
        for f in (
                self.store, self.summary, self.category, self.priority, self.dtstart, self.due, self.status,
                self.progress, self.completed, self.url, self.location, self.class_, self.description,
                self.created, self.dtstamp, self.modified
        ):
            f.clear()


class TodoSortWidget(QtWidgets.QGroupBox):
    by_asis: QtWidgets.QRadioButton
    by_name: QtWidgets.QRadioButton
    by_pdn: QtWidgets.QRadioButton
    bg: QtWidgets.QButtonGroup

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Sort")
        # widgets
        self.by_asis = QtWidgets.QRadioButton("As is", self)
        self.by_name = QtWidgets.QRadioButton("Name", self)
        self.by_pdn = QtWidgets.QRadioButton("!→Due→Name", self)
        # logic
        self.bg = QtWidgets.QButtonGroup(self)
        self.bg.addButton(self.by_asis, enums.ESortBy.AsIs)
        self.bg.addButton(self.by_name, enums.ESortBy.Name)
        self.bg.addButton(self.by_pdn, enums.ESortBy.PrioDueName)
        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.by_asis)
        layout.addWidget(self.by_name)
        layout.addWidget(self.by_pdn)
        # layout.addStretch(1);
        self.setLayout(layout)
        # the end
        self.by_asis.setChecked(True)


class TodoFilterWidget(QtWidgets.QGroupBox):
    f_All: QtWidgets.QRadioButton
    f_Closed: QtWidgets.QRadioButton
    f_Opened: QtWidgets.QRadioButton
    f_Today: QtWidgets.QRadioButton
    f_Tomorrow: QtWidgets.QRadioButton
    bg: QtWidgets.QButtonGroup

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Filter")
        # widgets
        self.f_All = QtWidgets.QRadioButton("All", self)
        self.f_Closed = QtWidgets.QRadioButton("Closed", self)
        self.f_Opened = QtWidgets.QRadioButton("Opened", self)
        self.f_Today = QtWidgets.QRadioButton("Today", self)
        self.f_Tomorrow = QtWidgets.QRadioButton("Tomorrow", self)
        # logic
        self.bg = QtWidgets.QButtonGroup(self)
        self.bg.addButton(self.f_All, enums.EFiltBy.All)
        self.bg.addButton(self.f_Closed, enums.EFiltBy.Closed)
        self.bg.addButton(self.f_Opened, enums.EFiltBy.Opened)
        self.bg.addButton(self.f_Today, enums.EFiltBy.Today)
        self.bg.addButton(self.f_Tomorrow, enums.EFiltBy.Tomorrow)
        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.f_All)
        layout.addWidget(self.f_Closed)
        layout.addWidget(self.f_Opened)
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
        # left_panel.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.addWidget(self.stores)
        left_layout.addWidget(self.l_sort)
        left_layout.addWidget(self.l_filt)
        # left_layout.addStretch(1)
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
        # self.stores.model().activeChanged.connect(self.list.model().sourceModel().updateFilterByStore)
        self.stores.model().activeChanged.connect(self.list.model().refilter)
        self.l_sort.bg.idClicked.connect(self.list.model().sortChanged)
        self.l_filt.bg.idClicked.connect(self.list.model().filtChanged)
