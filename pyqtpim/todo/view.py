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
    def _empty_model(self) -> TodoListModel:
        return TodoListModel()


class TodoView(EntryView):
    summary: QtWidgets.QLineEdit
    completed: QtWidgets.QDateTimeEdit
    dtstart: QtWidgets.QDateTimeEdit
    due: QtWidgets.QDateTimeEdit
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
        self.class_ = QtWidgets.QLineEdit(self)
        self.completed = QtWidgets.QDateTimeEdit(self)
        self.dtstart = QtWidgets.QDateTimeEdit(self)
        self.due = QtWidgets.QDateTimeEdit(self)
        self.percent = QtWidgets.QSpinBox(self)
        self.percent.setMaximum(100)
        self.prio = QtWidgets.QSpinBox(self)
        self.status = QtWidgets.QLineEdit(self)
        self.trans = QtWidgets.QLineEdit(self)
        # layout
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Summary:"), self.summary)
        layout.addRow(QtWidgets.QLabel("Class:"), self.class_)
        layout.addRow(QtWidgets.QLabel("Complete:"), self.completed)
        layout.addRow(QtWidgets.QLabel("DTStart:"), self.dtstart)
        layout.addRow(QtWidgets.QLabel("Due:"), self.due)
        layout.addRow(QtWidgets.QLabel("%:"), self.percent)
        layout.addRow(QtWidgets.QLabel("Prio:"), self.prio)
        layout.addRow(QtWidgets.QLabel("Status:"), self.status)
        layout.addRow(QtWidgets.QLabel("Trans:"), self.trans)
        self.setLayout(layout)
        # attributes
        self.summary.setReadOnly(True)
        self.class_.setReadOnly(True)
        self.completed.setReadOnly(True)
        self.dtstart.setReadOnly(True)
        self.due.setReadOnly(True)
        self.percent.setReadOnly(True)
        self.prio.setReadOnly(True)
        self.status.setReadOnly(True)
        self.trans.setReadOnly(True)

    def setModel(self, model: QtCore.QStringListModel):
        """Setup mapper
        :todo: indexOf
        """
        self.mapper.setModel(model)
        self.mapper.addMapping(self.summary, 0)
        self.mapper.addMapping(self.class_, 1)
        self.mapper.addMapping(self.completed, 2)
        self.mapper.addMapping(self.dtstart, 3)
        self.mapper.addMapping(self.due, 4)
        self.mapper.addMapping(self.percent, 5)
        self.mapper.addMapping(self.prio, 6)
        self.mapper.addMapping(self.status, 7)
        self.mapper.addMapping(self.trans, 8)

    def clean(self):
        # print("Details clean call")
        self.summary.clear()
        self.class_.clear()
        self.completed.clear()
        self.dtstart.clear()
        self.due.clear()
        self.percent.clear()
        self.prio.clear()
        self.status.clear()
        self.trans.clear()


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
