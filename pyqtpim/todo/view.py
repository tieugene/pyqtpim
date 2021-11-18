"""GUI representation of ToDo things"""

from PySide2 import QtCore, QtWidgets
# 3. local
from common import EntryDetailWidget, EntryListView, EntryListManagerView
from .model import TodoListManagerModel, TodoListModel


class TodoListManagerView(EntryListManagerView):
    _title = 'ToDo list'

    def _empty_model(self) -> TodoListManagerModel:
        return TodoListManagerModel()


class TodoListView(EntryListView):
    def _empty_model(self) -> TodoListModel:
        return TodoListModel()


class TodoDetailWidget(EntryDetailWidget):
    summary: QtWidgets.QLineEdit

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Details")
        self.__createWidgets()

    def __createWidgets(self):
        # order
        self.summary = QtWidgets.QLineEdit(self)
        # layout
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Summary:"), self.summary)
        self.setLayout(layout)
        # attributes
        self.summary.setReadOnly(True)

    def setModel(self, model: QtCore.QStringListModel):
        """Setup mapper"""
        self.mapper.setModel(model)
        self.mapper.addMapping(self.summary, 0)

    def clean(self):
        # print("Details clean call")
        self.summary.clear()


class TodosWidget(QtWidgets.QWidget):
    sources: TodoListManagerView
    list: TodoListView
    details: TodoDetailWidget

    def __init__(self):
        super().__init__()
        self.__createWidgets()

    def __createWidgets(self):
        # order
        splitter = QtWidgets.QSplitter(self)
        self.details = TodoDetailWidget(splitter)
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


class TodoCUDialog(QtWidgets.QDialog):
    ...
