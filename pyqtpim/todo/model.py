# 1. system
# 2. PySide
import datetime
import os
from typing import Any, Callable, Optional, Union
# 2. PySide2
from PySide2 import QtCore, QtSql
# 3. 3rd
import vobject
# 4. local
from common import SetGroup, EntryModel, EntryProxyModel, StoreModel, exc
from .data import VObjTodo
from . import enums, query


class TodoModel(EntryModel):
    """todo: collect categories/locations on load"""
    __entry_cache: dict[int, VObjTodo]  # entry.id: VObj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__entry_cache = dict()
        self.setTable("entry")
        for i in range(len(enums.ColHeader)):
            self.setHeaderData(i, QtCore.Qt.Horizontal, enums.ColHeader[i])
        self.updateFilterByStore()
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
            v = super().data(idx, role)
            col = idx.column()
            if col == enums.EColNo.Prio.value:
                if v:  # :str()|int
                    return enums.TDecor_Prio[v - 1]
            elif col == enums.EColNo.Status.value:
                if v:  # :str()|int
                    return enums.TDecor_Status[v - 1]
            elif col == enums.EColNo.Store.value:
                return self.store_name[v]  # v:int
            elif col == enums.EColNo.Created.value:
                return __utc2disp(v)  # v:str
            elif col == enums.EColNo.DTStamp.value:
                return __utc2disp(v)  # v:str
            elif col == enums.EColNo.Modified.value:
                return __utc2disp(v)  # v:str
            elif col == enums.EColNo.Completed.value:
                return __utc2disp(v)  # v:str
            elif col == enums.EColNo.DTStart.value:
                return __vardatime2disp(v)  # v:str
            elif col == enums.EColNo.Due.value:
                return __vardatime2disp(v)  # v:str
            elif col == enums.EColNo.Syn.value:
                return enums.TDecor_Syn[v - 1]
            else:
                # print("v:", v, type(v))
                return v
        elif role == QtCore.Qt.ForegroundRole:
            v = super().data(idx, QtCore.Qt.DisplayRole)
            col = idx.column()
            if col == enums.EColNo.Prio.value:
                if v:
                    return enums.TColor_Prio[v - 1]
            if col == enums.EColNo.Status.value:
                if v:
                    return enums.TColor_Status[v - 1]
            if col == enums.EColNo.Syn.value:
                if v:
                    return enums.TColor_Syn[v - 1]
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
        q: QtSql.QSqlQuery = QtSql.QSqlQuery('SELECT id FROM store WHERE active IS TRUE')
        while q.next():
            active.add(q.value(0))
        if active:
            if len(active) == 1:
                filt = 'store_id = %d' % active.pop()
            else:
                filt = 'store_id IN %s' % str(tuple(active))
        else:
            filt = 'FALSE'  # nothing to show
        self.setFilter(filt)

    def reloadAll(self, store_id: int, store_path: str):
        self.beginResetModel()
        if QtSql.QSqlQuery(query.entry_drop_all % store_id):  # FIXME: clean obj cache
            load_store(self, store_id, store_path)
        else:
            print("Error clean store's entries")
        self.endResetModel()


class TodoProxyModel(EntryProxyModel):
    _own_model = TodoModel
    __currentSorter: Callable
    __currentFilter: Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__currentSort = self.__lessThen_ID
        self.__currentFilter = self.__accept_All
        self.setDynamicSortFilter(True)
        # TODO: self.resizeColumntToContent(*)
        self.__today = datetime.date.today()
        self.__tomorrow = self.__today + datetime.timedelta(days=1)

    # Inherit
    def lessThan(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """:todo: combine per-column built-in sort with complex one"""
        return self.__currentSort(source_left, source_right)

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        """Default: all; Today: Due <= today [todo: and not completed]"""
        return self.__currentFilter(source_row)

    # Hand-made
    def sortChanged(self, sort_id: enums.ESortBy):
        self.beginResetModel()
        self.__currentSort = {
            enums.ESortBy.ID: self.__lessThen_ID,
            enums.ESortBy.Name: self.__lessThen_Name,
            enums.ESortBy.PrioDueName: self.__lessThen_PrioDueName
        }[sort_id]
        self.endResetModel()

    def filtChanged(self, filt_id: enums.EFiltBy):
        self.__currentFilter = {
            enums.EFiltBy.All: self.__accept_All,
            enums.EFiltBy.Closed: self.__accept_Closed,
            enums.EFiltBy.Today: self.__accept_Today,
            enums.EFiltBy.Tomorrow: self.__accept_Tomorrow
        }[filt_id]
        # print("Filter changed:", filt_id)
        self.invalidateFilter()

    def __lessThen_ID(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        realmodel = self.sourceModel()
        data_left = realmodel.data(realmodel.index(source_left.row(), enums.EColNo.ID.value))
        data_right = realmodel.data(realmodel.index(source_right.row(), enums.EColNo.ID.value))
        return data_right < data_left

    def __lessThen_Name(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        realmodel = self.sourceModel()
        data_left = realmodel.data(realmodel.index(source_left.row(), enums.EColNo.Summary.value))
        data_right = realmodel.data(realmodel.index(source_right.row(), enums.EColNo.Summary.value))
        return data_right < data_left

    def __lessThen_PrioDueName(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """Sorting Prio>Due>Summary"""

        def __get_prio(vobj: VObjTodo) -> int:
            if v := vobj.get_Priority():
                return enums.Raw2Enum_Prio[v]
            else:
                return 0

        def __get_due_date(vobj: VObjTodo) -> datetime.date:
            if v := vobj.get_Due():
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
        return obj_right.get_Summary() < obj_left.get_Summary()

    @staticmethod
    def __accept_All(_: int) -> bool:
        """Enable all ToDos"""
        return True

    def __accept_Closed(self, source_row: int) -> bool:
        """Show only Status=Complete[|Cancelled]"""
        return self.sourceModel().getObj(source_row).get_Status() in {enums.EStatus.Completed, enums.EStatus.Cancelled}

    def __accept_Today(self, source_row: int) -> bool:
        """Show only ~(Complete|Cancelled) & Due & Due <= today"""
        closed = {enums.EStatus.Completed, enums.EStatus.Cancelled}

        vobj: VObjTodo = self.sourceModel().getObj(source_row)
        return (vobj.get_Status() not in closed) and (due := vobj.get_Due_as_date()) is not None and due <= self.__today

    def __accept_Tomorrow(self, source_row: int) -> bool:
        """Like today but tomorrow"""
        closed = {enums.EStatus.Completed, enums.EStatus.Cancelled}
        vobj: VObjTodo = self.sourceModel().getObj(source_row)
        return (vobj.get_Status() not in closed) and (due := vobj.get_Due_as_date()) is not None and due <= self.__tomorrow


class TodoStoreModel(StoreModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.ToDo


def load_store(model: TodoModel, store_id: int, path: str):
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
                        q = obj2sql(query.entry_add, obj)
                        q.bindValue(':store_id', store_id)
                        q.bindValue(':syn', enums.ESyn.Synced.value)
                        if not q.exec_():
                            print(f"Something bad with adding record '{obj.get_Summary()}': {q.lastError().text()}")
                        # else:
                        #     print(f"Record #{q.lastInsertId()} added")
                        #     model.addObj(q.lastInsertId(), obj)
                else:
                    raise exc.EntryLoadError(f"Cannot load vobject: {entry.path}")
    model.select()


def obj2sql(q_str: str, vobj: VObjTodo) -> QtSql.QSqlQuery:
    def __2Z(__v: Optional[datetime.datetime]) -> str:
        if __v:
            return __v.replace(tzinfo=datetime.timezone.utc).isoformat()

    def __2iso(__v: Optional[Union[datetime.date, datetime.datetime]]) -> str:
        if __v:
            return __v.isoformat()

    q = QtSql.QSqlQuery()
    q.prepare(q_str)
    q.bindValue(':created', __2Z(vobj.get_Created()))
    q.bindValue(':dtstamp', __2Z(vobj.get_DTStamp()))
    q.bindValue(':modified', __2Z(vobj.get_LastModified()))
    q.bindValue(':dtstart', __2iso(vobj.get_DTStart()))
    q.bindValue(':due', __2iso(vobj.get_Due()))
    q.bindValue(':completed', __2iso(vobj.get_Completed()))  # ?
    q.bindValue(':progress', vobj.get_Progress())
    q.bindValue(':priority', enums.Raw2Enum_Prio[v] if (v := vobj.get_Priority()) else None)
    q.bindValue(':status', vobj.get_Status())
    q.bindValue(':summary', vobj.get_Summary())
    q.bindValue(':location', vobj.get_Location())
    q.bindValue(':body', vobj.serialize())
    return q
