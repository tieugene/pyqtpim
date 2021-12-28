# 1. system
# 2. PySide
import datetime
from typing import Any, Optional, Union
# 2. PySide2
from PySide2 import QtCore, QtSql
# 3. 3rd
import vobject
# 4. local
from common import EntryModel, EntryProxyModel, StoreModel, SetGroup
from .data import TodoVObj, TodoStore, store_list, entry_list
from . import enums


class TodoModel(EntryModel):
    """todo: collect categories/locations on load"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = entry_list
        self.updateFilterByStore()

    # Inherit
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.DisplayRole:
            return enums.ColHeader[section]

    def columnCount(self, parent: QtCore.QModelIndex = None) -> int:
        return len(enums.ColHeader)

    def data(self, idx: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        def __utc2disp(data: Optional[datetime.datetime]) -> str:
            """Convert UTC datetime into viewable localtime"""
            if data:
                return data.replace(tzinfo=None).isoformat(sep=' ', timespec='minutes')

        def __vardatime2disp(data: Optional[Union[datetime.datetime, datetime.date]]) -> str:
            """Convert datetime (naive/tzed) into viewable localtime"""
            if data:
                if isinstance(data, datetime.datetime):
                    return data.replace(tzinfo=None).isoformat(sep=' ', timespec='minutes')
                else:  # date => no convert
                    return data.isoformat()

        if not idx.isValid():
            return None
        entry = self._data.entry_get(idx.row())
        vobj: TodoVObj = entry.vobj
        col = idx.column()
        if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:
            if col == enums.EColNo.Store.value:
                return entry.store.name
            if col == enums.EColNo.Created.value:
                return __utc2disp(vobj.get_Created())
            elif col == enums.EColNo.DTStamp.value:
                return __utc2disp(vobj.get_DTStamp())
            elif col == enums.EColNo.Modified.value:
                return __utc2disp(vobj.get_LastModified())
            elif col == enums.EColNo.DTStart.value:
                return __vardatime2disp(vobj.get_DTStart())
            elif col == enums.EColNo.Due.value:
                return __vardatime2disp(vobj.get_Due())
            elif col == enums.EColNo.Completed.value:
                return __utc2disp(vobj.get_Completed())
            elif col == enums.EColNo.Progress.value:
                return vobj.get_Progress()
            elif col == enums.EColNo.Prio.value:
                if v := vobj.get_Priority():
                    return enums.TDecor_Prio[v - 1]
            elif col == enums.EColNo.Status.value:
                if v := vobj.get_Status():
                    return enums.TDecor_Status[v - 1]
            elif col == enums.EColNo.Summary.value:
                return vobj.get_Summary()
            elif col == enums.EColNo.Location.value:
                return vobj.get_Location()
        '''
        elif role == QtCore.Qt.EditRole:
            col = idx.column()
            if col == enums.EColNo.Completed.value:
                return self.data(idx, QtCore.Qt.DisplayRole)
            else:
                return super().data(idx, role)
        elif role == QtCore.Qt.ForegroundRole:
            # v = super().data(idx, QtCore.Qt.DisplayRole)
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
            # return super().data(idx, role)
        # else:
            # return super().data(idx, role)
        '''

    # Hand-made
    # def reload(self):
    #    self.beginResetModel()
    #    self.endResetModel()

    def getObjByRow(self, row: int):
        """Get [cached] entry body.
        Callers: TodoListView.entryEdit(), .entryInside()
        """
        entry_id = self.data(self.index(row, enums.EColNo.ID))
        if rec := self.record(row):
            _id = rec.value('id')
            if (v := self.__entry_cache.get(entry_id)) is None:
                v = TodoVObj(vobject.readOne(self.data(self.index(row, enums.EColNo.Body))))
                self.__entry_cache[entry_id] = v
            return v

    def updateFilterByStore(self):
        """"""
        ...
        # self.reload()


class TodoProxyModel(EntryProxyModel):
    # _own_model = TodoModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDynamicSortFilter(True)
        # TODO: self.resizeColumntToContent(*)
        self.__today = datetime.date.today()
        self.__tomorrow = self.__today + datetime.timedelta(days=1)

    # Inherit
    def lessThan(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """:todo: combine per-column built-in sort with complex one"""
        # print("lessThen")
        return self._currentSorter(source_left, source_right)

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        """Default: all; Today: Due <= today [todo: and not completed]"""
        return self._currentFilter(source_row)

    # Hand-made
    def sortChanged(self, sort_id: enums.ESortBy):
        # self.beginResetModel()
        self._currentSorter = {
            enums.ESortBy.AsIs: self._lessThen_None,
            enums.ESortBy.Name: self.__lessThen_Name,
            enums.ESortBy.PrioDueName: self.__lessThen_PrioDueName
        }[sort_id]
        # self.endResetModel()
        self.invalidate()
        # self.parent().requery()

    def filtChanged(self, filt_id: enums.EFiltBy):
        self._currentFilter = {
            enums.EFiltBy.All: self._accept_All,
            enums.EFiltBy.Closed: self.__accept_Closed,
            enums.EFiltBy.Today: self.__accept_Today,
            enums.EFiltBy.Tomorrow: self.__accept_Tomorrow
        }[filt_id]
        # print("Filter changed:", filt_id)
        self.invalidateFilter()
        self.parent().requery()

    def __lessThen_Name(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        realmodel = self.sourceModel()
        # data_left = realmodel.data(realmodel.index(source_left.row(), enums.EColNo.Summary.value))
        # data_right = realmodel.data(realmodel.index(source_right.row(), enums.EColNo.Summary.value))
        data_left = realmodel.item_get(source_left.row()).vobj.get_Summary()
        data_right = realmodel.item_get(source_right.row()).vobj.get_Summary()
        return data_right.casefold() < data_left.casefold()

    def __lessThen_PrioDueName(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """Sorting Prio>Due>Summary"""
        def __get_prio(vobj: TodoVObj) -> int:
            if v := vobj.get_Priority():
                return enums.Raw2Enum_Prio[v]
            else:
                return 0

        def __get_due_date(vobj: TodoVObj) -> datetime.date:
            if v := vobj.get_Due():
                if isinstance(v, datetime.datetime):
                    return v.date()
                return v
            return datetime.date(9999, 12, 31)

        realmodel = self.sourceModel()
        obj_left: TodoVObj = realmodel.item_get(source_left.row()).vobj
        obj_right: TodoVObj = realmodel.item_get(source_right.row()).vobj
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
        return obj_right.get_Summary().casefold() < obj_left.get_Summary().casefold()

    def __accept_Closed(self, source_row: int) -> bool:
        """Show only Status=Complete[|Cancelled]"""
        return self.sourceModel().getObjByRow(source_row).get_Status() in {enums.EStatus.Completed,
                                                                           enums.EStatus.Cancelled}

    def __accept_Today(self, source_row: int) -> bool:
        """Show only ~(Complete|Cancelled) & Due & Due <= today"""
        closed = {enums.EStatus.Completed, enums.EStatus.Cancelled}
        vobj: TodoVObj = self.sourceModel().getObjByRow(source_row)
        due = vobj.get_Due_as_date()
        return (vobj.get_Status() not in closed) and due is not None and due <= self.__today

    def __accept_Tomorrow(self, source_row: int) -> bool:
        """Like today but tomorrow"""
        closed = {enums.EStatus.Completed, enums.EStatus.Cancelled}
        vobj: TodoVObj = self.sourceModel().getObjByRow(source_row)
        due = vobj.get_Due_as_date()
        return \
            (vobj.get_Status() not in closed) \
            and due is not None \
            and due <= self.__tomorrow


class TodoStoreModel(StoreModel):
    item_cls = TodoStore

    def __init__(self, entries: TodoModel, *args, **kwargs):
        super().__init__(entries, *args, **kwargs)
        self._set_group = SetGroup.ToDo
        self._data = store_list


def obj2sql(q_str: str, vobj: TodoVObj) -> QtSql.QSqlQuery:
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
    q.bindValue(':status', v.value if (v := vobj.get_Status()) else None)
    q.bindValue(':summary', vobj.get_Summary())
    q.bindValue(':location', vobj.get_Location())
    q.bindValue(':body', vobj.serialize())
    return q


todo_model = TodoModel()
store_model = TodoStoreModel(todo_model)
