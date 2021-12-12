# 1. system
# 2. PySide
import vobject
from PySide2 import QtCore, QtSql
# 3. local
from common import SetGroup, EntryModel, StoreModel
from .data import VObjTodo


class TodoModel(EntryModel):
    """todo: collect categories/locations on load"""
    __entry_cache: dict[int, VObjTodo]    # entry.id: VObj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__entry_cache = dict()
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
        self.updateFilterByStore()
        self.select()

    def setObj(self, rec: QtSql.QSqlRecord, obj: VObjTodo):
        """Add entry body to cache"""
        self.__entry_cache[rec.value('id')] = obj

    def getObj(self, row: int):
        """Get [cached] entry body"""
        if rec := self.record(row):
            _id = rec.value('id')
            if (v := self.__entry_cache.get(_id)) is None:
                v = VObjTodo(vobject.readOne(rec.value('body')))
                self.__entry_cache[_id] = v
            return v

    def delObj(self, row: int):
        """Del entry body from cache"""
        if rec := self.record(row):
            _id = rec.value('_id')
            if _id in self.__entry_cache:
                del self.__entry_cache[_id]

    def updateFilterByStore(self):
        """"""
        active = set()
        query: QtSql.QSqlQuery = QtSql.QSqlQuery('SELECT id FROM store WHERE active IS TRUE')
        while query.next():
            active.add(query.value(0))
        if active:
            if len(active) == 1:
                filt = 'store_id = %d' % active.pop()
            else:
                filt = 'store_id IN %s' % str(tuple(active))
        else:
            filt = 'FALSE'  # nothing to show
        self.setFilter(filt)


class TodoStoreModel(StoreModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo


def obj2rec(obj: VObjTodo, rec: QtSql.QSqlRecord, store_id: int):
    """Create new record and fill it with ventry content"""
    rec.setValue('store_id', store_id)
    rec.setValue('created', obj.getCreated().isoformat())
    rec.setValue('modified', obj.getLastModified().isoformat())
    if v := obj.getDTStart():
        rec.setValue('dtstart', v.isoformat())
    if v := obj.getDue():
        rec.setValue('due', v.isoformat())
    if v := obj.getCompleted():
        rec.setValue('completed', v.isoformat())
    if not (v := obj.getPercent()) is None:
        rec.setValue('progress', v)
    if not (v := obj.getPriority()) is None:
        rec.setValue('priority', v)
    if v := obj.getStatus():
        rec.setValue('status', v.value)
    rec.setValue('summary', obj.getSummary())
    if v := obj.getLocation():
        rec.setValue('location', v)
    rec.setValue('body', obj.serialize())
