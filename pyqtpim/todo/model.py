# 1. system
# 2. PySide
import datetime
from typing import Any, Callable

import vobject
from PySide2 import QtCore, QtSql
# 3. local
from common import SetGroup, EntryModel, EntryProxyModel, StoreModel
from .data import VObjTodo
from . import enums


class TodoModel(EntryModel):
    """todo: collect categories/locations on load"""
    __entry_cache: dict[int, VObjTodo]  # entry.id: VObj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__entry_cache = dict()
        self.setTable("entry")
        # self.setRelation(self.fieldIndex('store_id'), QtSql.QSqlRelation('store', 'id', 'name'))
        for i in range(len(enums.ColHeader)):
            self.setHeaderData(i, QtCore.Qt.Horizontal, enums.ColHeader[i])
        self.setHeaderData(self.fieldIndex('body'), QtCore.Qt.Horizontal, "Body")
        self.updateFilterByStore()
        # self.setSort(self.fieldIndex('priority'), QtCore.Qt.SortOrder.AscendingOrder)
        self.select()

    # Inherit
    def data(self, idx: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        def __utc2disp(data: str):
            """Convert UTC datetime into viewable localtime"""
            if data:
                return datetime.datetime.fromisoformat(data).astimezone().replace(tzinfo=None).isoformat(sep=' ')

        def __vardatime2disp(data: str):
            """Convert datetime (naive/tzed) into viewable localtime"""
            if data:
                if isinstance(datime := datetime.datetime.fromisoformat(data), datetime.datetime):
                    if datime.tzinfo:
                        return datime.astimezone().replace(tzinfo=None).isoformat(sep=' ', timespec='minutes')
                    else:  # naive => as is, w/o seconds
                        return data.replace('T', ' ')[:16]
                else:  # date => no convert
                    return data

        if not idx.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            col = idx.column()
            rec = self.record(idx.row())
            if col == self.fieldIndex('priority'):
                if v := rec.value('priority'):
                    return enums.TDecor_Prio[v]
            elif col == self.fieldIndex('status'):
                if v := rec.value('status'):
                    return enums.TDecor_Status[v]
            elif col == self.fieldIndex('store_id'):
                return self.store_name[rec.value('store_id')]
            elif col == self.fieldIndex('created'):
                return __utc2disp(rec.value('created'))
            elif col == self.fieldIndex('modified'):
                return __utc2disp(rec.value('modified'))
            elif col == self.fieldIndex('completed'):
                return __utc2disp(rec.value('completed'))
            elif col == self.fieldIndex('dtstart'):
                return __vardatime2disp(rec.value('dtstart'))
            elif col == self.fieldIndex('due'):
                return __vardatime2disp(rec.value('due'))
            else:
                return super().data(idx, role)
        elif role == QtCore.Qt.ForegroundRole:
            col = idx.column()
            rec = self.record(idx.row())
            if col == self.fieldIndex('priority'):
                if v := rec.value('priority'):
                    return enums.TColor_Prio[v]
            if col == self.fieldIndex('status'):
                if v := rec.value('status'):
                    return enums.TColor_Status[v]
            return super().data(idx, role)
        else:
            return super().data(idx, role)

    # Hand-made
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


class TodoProxyModel(EntryProxyModel):
    _own_model = TodoModel
    __currentSorter: Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__currentSort = self.__lessThen_ID
        self.setDynamicSortFilter(True)
        # TODO: self.resizeColumntToContent(*)

    def __lessThen_ID(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        realmodel = self.sourceModel()
        data_left = realmodel.data(realmodel.index(source_left.row(), realmodel.fieldIndex('id')))
        data_right = realmodel.data(realmodel.index(source_right.row(), realmodel.fieldIndex('id')))
        return data_right < data_left

    def __lessThen_Name(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        realmodel = self.sourceModel()
        data_left = realmodel.data(realmodel.index(source_left.row(), realmodel.fieldIndex('summary')))
        data_right = realmodel.data(realmodel.index(source_right.row(), realmodel.fieldIndex('summary')))
        return data_right < data_left

    def __lessThen_PrioDueName(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """Sorting Prio>Due>Summary"""

        def __get_prio(vobj: VObjTodo) -> int:
            if v := vobj.getPriority():
                return enums.Raw2Enum_Prio[v]
            else:
                return 0

        def __get_due_date(vobj: VObjTodo) -> datetime.date:
            if v := vobj.getDue():
                if isinstance(v, datetime.datetime):
                    return v.date()
                return v
            return datetime.date(9999, 12, 31)

        realmodel = self.sourceModel()
        obj_left: VObjTodo = realmodel.getObj(source_left.row())
        obj_right: VObjTodo = realmodel.getObj(source_right.row())
        # 1. Prio
        prio_left = __get_prio(obj_left)
        prio_right = __get_prio(obj_right)
        if prio_left != prio_right:
            return prio_left < prio_right
        # 2. Due
        due_left = __get_due_date(obj_left)
        due_right = __get_due_date(obj_left)
        if due_left != due_right:
            return due_left < due_right
        # 3. Summary
        return obj_right.getSummary() < obj_left.getSummary()

    # Inherit
    def lessThan(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """:todo: combine per-column built-in sort with complex one"""
        return self.__currentSort(source_left, source_right)
        # return False

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        """Default: all; Today: Due <= today [todo: and not completed]"""
        return True
        today = datetime.date.today()
        due: str = self.sourceModel().data(self.sourceModel().index(source_row, self.sourceModel().fieldIndex('due')))
        if due:
            return datetime.date.fromisoformat(due) <= today
        else:
            return False

    # Hand-made
    def sortChanged(self, sort_id: enums.ESortBy):
        self.beginResetModel()
        self.__currentSort = {
            enums.ESortBy.ID: self.__lessThen_ID,
            enums.ESortBy.Name: self.__lessThen_Name,
            enums.ESortBy.PrioDueName: self.__lessThen_PrioDueName
        }[sort_id]
        self.endResetModel()


class TodoStoreModel(StoreModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo


def obj2rec(obj: VObjTodo, rec: QtSql.QSqlRecord, store_id: int):
    """Create new record and fill it with ventry content"""
    rec.setValue('store_id', store_id)
    rec.setValue('created', obj.getCreated().replace(tzinfo=datetime.timezone.utc).isoformat())
    rec.setValue('modified', obj.getLastModified().replace(tzinfo=datetime.timezone.utc).isoformat())
    if v := obj.getDTStart():
        rec.setValue('dtstart', v.isoformat())
    if v := obj.getDue():
        rec.setValue('due', v.isoformat())
    if v := obj.getCompleted():
        rec.setValue('completed', v.isoformat())
    if not (v := obj.getPercent()) is None:
        rec.setValue('progress', v)
    if v := obj.getPriority():
        rec.setValue('priority', enums.Raw2Enum_Prio[v])
    if v := obj.getStatus():
        rec.setValue('status', v.value)
    rec.setValue('summary', obj.getSummary())
    if v := obj.getLocation():
        rec.setValue('location', v)
    body = obj.serialize()
    rec.setValue('body', body)
