"""GUI representation of ToDo things"""

from PySide2 import QtCore, QtWidgets
# 3. local
from common import EntryView, EntryListView, EntryListManagerView
from .model import TodoListManagerModel, TodoListModel


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


class TodoView(EntryView):
    summary: QtWidgets.QLineEdit
    categories: QtWidgets.QPlainTextEdit
    completed: QtWidgets.QDateTimeEdit
    dtstart: QtWidgets.QDateTimeEdit
    due: QtWidgets.QDateTimeEdit
    location: QtWidgets.QLineEdit
    percent: QtWidgets.QSpinBox
    prio: QtWidgets.QSpinBox
    status: QtWidgets.QLineEdit

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Details")
        self.__createWidgets()

    def __createWidgets(self):
        # order
        self.summary = QtWidgets.QLineEdit(self)
        self.categories = QtWidgets.QPlainTextEdit(self)
        self.completed = QtWidgets.QDateTimeEdit(self)
        self.dtstart = QtWidgets.QDateTimeEdit(self)
        self.due = QtWidgets.QDateTimeEdit(self)
        self.location = QtWidgets.QLineEdit(self)
        self.percent = QtWidgets.QSpinBox(self)
        self.prio = QtWidgets.QSpinBox(self)
        self.status = QtWidgets.QLineEdit(self)
        # layout
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Summary:"), self.summary)
        layout.addRow(QtWidgets.QLabel("Categories:"), self.categories)
        layout.addRow(QtWidgets.QLabel("Complete:"), self.completed)
        layout.addRow(QtWidgets.QLabel("DTStart:"), self.dtstart)
        layout.addRow(QtWidgets.QLabel("Due:"), self.due)
        layout.addRow(QtWidgets.QLabel("Location:"), self.location)
        layout.addRow(QtWidgets.QLabel("%:"), self.percent)
        layout.addRow(QtWidgets.QLabel("Prio:"), self.prio)
        layout.addRow(QtWidgets.QLabel("Status:"), self.status)
        self.setLayout(layout)
        # attributes
        self.summary.setReadOnly(True)
        self.categories.setReadOnly(True)
        self.completed.setReadOnly(True)
        self.dtstart.setReadOnly(True)
        self.due.setReadOnly(True)
        self.location.setReadOnly(True)
        self.percent.setReadOnly(True)
        self.prio.setReadOnly(True)
        self.status.setReadOnly(True)
        # misc
        self.percent.setMaximum(100)

    def __idxChgd(self, idx: int):
        """Only for selection; not calling on deselection"""
        print("Idx chgd:", idx)
        self.mapper.model().item(idx)

    def setModel(self, model: QtCore.QStringListModel):
        """Setup mapper
        :todo: indexOf
        """
        super().setModel(model)
        self.mapper.addMapping(self.summary, 0)
        self.mapper.addMapping(self.categories, 1)
        self.mapper.addMapping(self.completed, 2)
        self.mapper.addMapping(self.dtstart, 3)
        self.mapper.addMapping(self.due, 4)
        self.mapper.addMapping(self.location, 5)
        self.mapper.addMapping(self.percent, 6)
        self.mapper.addMapping(self.prio, 7)
        self.mapper.addMapping(self.status, 8)
        self.mapper.currentIndexChanged[int].connect(self.__idxChgd)

    def clean(self):
        # print("Details clean call")
        self.summary.clear()
        self.categories.clear()
        self.completed.clear()
        self.dtstart.clear()
        self.due.clear()
        self.location.clear()
        self.percent.clear()
        self.prio.clear()
        self.status.clear()


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


class TodoForm(QtWidgets.QDialog):
    ...
