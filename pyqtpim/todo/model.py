# 1. system
# 2. PySide
import vobject
from PySide2 import QtCore, QtSql
# 3. local
from common import SetGroup, EntryListModel, EntryListManagerModel
from .data import VObjTodo
from . import enums


class TodoListModel(EntryListModel):
    __entry_cache: dict[int, vobject.base.Component]
    __types = set()  # temp types cache
    __DemapClass = {
        enums.EClass.Public: "Do something",
        enums.EClass.Private: "wait...",
        enums.EClass.Confidential: "OK"
    }
    __DemapStatus = {
        enums.EStatus.NeedsAction: "Do something",
        enums.EStatus.InProcess: "wait...",
        enums.EStatus.Completed: "OK",
        enums.EStatus.Cancelled: "WontFix",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__entry_cache = dict()
        # self._data = TodoList()
        self.setTable("entry")
        # self.setRelation(self.fieldIndex('store_id'), QtSql.QSqlRelation('store', 'id', 'name'))
        self.setHeaderData(self.fieldIndex('id'), QtCore.Qt.Horizontal, 'ID')
        self.setHeaderData(self.fieldIndex('store_id'), QtCore.Qt.Horizontal, 'store')
        self.setHeaderData(self.fieldIndex('created'), QtCore.Qt.Horizontal, "Created")
        self.setHeaderData(self.fieldIndex('modified'), QtCore.Qt.Horizontal, "Updated")
        self.setHeaderData(self.fieldIndex('dtstart'), QtCore.Qt.Horizontal, "DTStart")
        self.setHeaderData(self.fieldIndex('due'), QtCore.Qt.Horizontal, "Due")
        self.setHeaderData(self.fieldIndex('completed'), QtCore.Qt.Horizontal, "Completed")
        self.setHeaderData(self.fieldIndex('progress'), QtCore.Qt.Horizontal, "%")
        self.setHeaderData(self.fieldIndex('priority'), QtCore.Qt.Horizontal, "Prio")
        self.setHeaderData(self.fieldIndex('status'), QtCore.Qt.Horizontal, "Status")
        self.setHeaderData(self.fieldIndex('summary'), QtCore.Qt.Horizontal, "Summary")
        self.setHeaderData(self.fieldIndex('location'), QtCore.Qt.Horizontal, "Loc")
        self.setHeaderData(self.fieldIndex('body'), QtCore.Qt.Horizontal, "Body")
        self.select()

    def getEntry(self, idx: int):
        """Get [cached] entry body"""
        if (v := self.__entry_cache.get(idx)) is None:
            v = VObjTodo(vobject.readOne(self.record(idx).value('body')))
            self.__entry_cache[idx] = v
        return v

    # def _empty_item(self) -> TodoList:
    #    return TodoList()

    # def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
    #     """
    #
    #     :param index:
    #     :param role:
    #     :return:
    #
    #     Types from uplink:
    #     - NoneType
    #     - int
    #     - str
    #     - PySide2.QtCore.QDate
    #     - PySide2.QtCore.QDateTime
    #     - EClass
    #     - EStatus
    #     """
    #     def __chk_type(_v: Any):
    #         t = type(_v)
    #         if t not in self.__types:
    #             self.__types.add(t)
    #             print(t)
    #     v = super().data(index, role)
    #     # __chk_type(v)
    #     # FIXME: too dumb selection
    #     if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:  # list/details
    #         if isinstance(v, enums.EClass):
    #             v = self.__DemapClass[v]
    #         elif isinstance(v, enums.EStatus):
    #             v = self.__DemapStatus[v]
    #         elif isinstance(v, list):
    #             if role == QtCore.Qt.DisplayRole:
    #                 v = ', '.join(v)
    #             else:
    #                 v = '\n'.join(v)
    #     return v


class TodoListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo
        # self._data = TodoListManager()
        # self._init_data()


def obj2rec(obj: VObjTodo, rec: QtSql.QSqlRecord):
    """Create new record and fill it with ventry content"""
    # rec: QtSql.QSqlRecord = self.record()
    rec.setValue('body', obj.serialize())
    rec.setValue('created', obj.getCreated().isoformat())
    rec.setValue('modified', obj.getLastModified().isoformat())
    rec.setValue('summary', obj.getSummary())
    if v := obj.getDTStart():
        rec.setValue('dtstart', v.isoformat())
    else:
        rec.setNull('dtstart')
    if v := obj.getDue():
        rec.setValue('due', v.isoformat())
    else:
        rec.setNull('due')
    if v := obj.getCompleted():
        rec.setValue('completed', v.isoformat())
    else:
        rec.setNull('completed')
    if not (v := obj.getPercent()) is None:
        rec.setValue('progress', v)
    else:
        rec.setNull('progress')
    if not (v := obj.getPriority()) is None:
        rec.setValue('priority', v)
    else:
        rec.setNull('priority')
    if v := obj.getStatus():
        rec.setValue('status', v.value)
    else:
        rec.setNull('status')
    if v := obj.getLocation():
        rec.setValue('location', v)
    else:
        rec.setNull('location')
    return rec
