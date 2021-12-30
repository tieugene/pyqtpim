# 1. system
# 2. PySide
import datetime
from typing import Any, Optional, Union
# 2. PySide2
from PySide2 import QtCore
# 3. 3rd
# 4. local
from common import EntryModel, EntryProxyModel, StoreModel, SetGroup
from .data import TodoVObj, TodoStore, store_list, entry_list
from . import enums

_today = datetime.date.today()
_yesterday = _today - datetime.timedelta(days=1)
_tomorrow = _today + datetime.timedelta(days=1)
_day_name = {
    _yesterday: "yest.",
    _today: "today",
    _tomorrow: "tomorw",
}


class TodoModel(EntryModel):
    """todo: collect categories/locations on load"""
    __datime_fmt = ('%d.%m %H:%M', '%d.%m.%y %H:%M')  # short, long
    __date_fmt = ('%d.%m', '%d.%m.%y')  # short, long

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = entry_list

    # Inherit
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
        if orientation == QtCore.Qt.Orientation.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return enums.ColHeader[section][0]
            elif role == QtCore.Qt.ToolTipRole:
                if tip := enums.ColHeader[section][1]:
                    return tip

    def columnCount(self, parent: QtCore.QModelIndex = None) -> int:
        return len(enums.ColHeader)

    def data(self, idx: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if not idx.isValid():
            return None
        entry = self._data.entry_get(idx.row())
        col = idx.column()
        if role in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:
            if col == enums.EColNo.Store.value:
                return entry.store.name
            else:
                return self.__data_display(col, entry.vobj, role)
        elif role == QtCore.Qt.ForegroundRole:  # == DislayRole | ForegroundRole
            return self.__data_foreground(col, entry.vobj)
        elif role == QtCore.Qt.TextAlignmentRole:
            if col in {enums.EColNo.Prio, enums.EColNo.Status}:
                return QtCore.Qt.AlignCenter
            elif col == enums.EColNo.Progress:
                return QtCore.Qt.AlignRight

    # Hand-made
    @staticmethod
    def __utc2disp(data: Optional[datetime.datetime]) -> Optional[str]:
        """Convert UTC datetime into viewable localtime"""
        if data:
            return data.astimezone().replace(tzinfo=None).strftime(TodoModel.__datime_fmt[1])
            # or .isoformat(sep=' ', timespec='minutes')

    @staticmethod
    def __vardatime2disp(data: Union[datetime.datetime, datetime.date], long: bool = False) -> str:
        """Convert datetime (naive/tzed) into viewable localtime"""
        if data:
            if isinstance(data, datetime.datetime):
                return data.replace(tzinfo=None).strftime(TodoModel.__datime_fmt[int(long)])
                # or .isoformat(sep=' ', timespec='minutes')
            else:  # date
                return data.strftime(TodoModel.__date_fmt[int(long)])
                # or .isoformat()

    def __data_display(self, col: int, vobj: TodoVObj, role: int) -> Optional[str]:
        if col == enums.EColNo.Created.value:
            return self.__utc2disp(vobj.get_Created())
        elif col == enums.EColNo.DTStamp.value:
            return self.__utc2disp(vobj.get_DTStamp())
        elif col == enums.EColNo.Modified.value:
            return self.__utc2disp(vobj.get_LastModified())
        elif col == enums.EColNo.DTStart.value:
            return self.__vardatime2disp(vobj.get_DTStart(), long=(role == QtCore.Qt.EditRole))
        elif col == enums.EColNo.Due.value:
            if role == QtCore.Qt.DisplayRole:
                if day_name := _day_name.get(vobj.get_Due_as_date()):
                    return day_name
            return self.__vardatime2disp(vobj.get_Due(), long=(role == QtCore.Qt.EditRole))
        elif col == enums.EColNo.Completed.value:
            return self.__utc2disp(vobj.get_Completed())
        elif col == enums.EColNo.Progress.value:
            if (v := vobj.get_Progress()) is not None:
                return str(v)
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

    def __data_edit(self, col: int, vobj: TodoVObj) -> str:
        ...

    @staticmethod
    def __data_foreground(col: int, vobj: TodoVObj) -> Any:
        if col == enums.EColNo.Prio.value:
            if v := vobj.get_Priority():
                return enums.TColor_Prio[v - 1]
        if col == enums.EColNo.Status.value:
            if v := vobj.get_Status():
                return enums.TColor_Status[v - 1]


class TodoProxyModel(EntryProxyModel):
    # _own_model = TodoModel
    __e_closed = {enums.EStatus.Completed, enums.EStatus.Cancelled}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDynamicSortFilter(True)
        # TODO: self.resizeColumntToContent(*)

    # Inherit
    def lessThan(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        """:todo: combine per-column built-in sort with complex one"""
        return self._currentSorter(source_left, source_right)

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        """Default: all; Today: Due <= today [todo: and not completed]"""
        return self._currentFilter(source_row)

    # Hand-made
    def sortChanged(self, sort_id: enums.ESortBy):
        self._currentSorter = {
            enums.ESortBy.AsIs: self._lessThen_None,
            enums.ESortBy.Name: self.__lessThen_Name,
            enums.ESortBy.PrioDueName: self.__lessThen_PrioDueName
        }[sort_id]
        self.invalidate()

    def filtChanged(self, filt_id: enums.EFiltBy):
        self._currentFilter = {
            enums.EFiltBy.All: self._accept_Default,
            enums.EFiltBy.Closed: self.__accept_Closed,
            enums.EFiltBy.Opened: self.__accept_Opened,
            enums.EFiltBy.Today: self.__accept_Today,
            enums.EFiltBy.Tomorrow: self.__accept_Tomorrow
        }[filt_id]
        self.invalidateFilter()

    def __lessThen_Name(self, source_left: QtCore.QModelIndex, source_right: QtCore.QModelIndex) -> bool:
        realmodel = self.sourceModel()
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
        entry = self.sourceModel().item_get(source_row)
        return entry.store.active and entry.vobj.get_Status() in self.__e_closed

    def __accept_Opened(self, source_row: int) -> bool:
        """Show only Status!=Complete[|Cancelled]"""
        entry = self.sourceModel().item_get(source_row)
        return entry.store.active and entry.vobj.get_Status() not in self.__e_closed

    def __accept_Today(self, source_row: int) -> bool:
        """Show only ~(Complete|Cancelled) & Due & Due <= today"""
        entry = self.sourceModel().item_get(source_row)
        vobj = entry.vobj
        due = vobj.get_Due_as_date()
        return\
            entry.store.active\
            and (vobj.get_Status() not in self.__e_closed)\
            and (due is not None)\
            and (due <= _today)

    def __accept_Tomorrow(self, source_row: int) -> bool:
        """Like today but tomorrow"""
        entry = self.sourceModel().item_get(source_row)
        vobj = entry.vobj
        due = vobj.get_Due_as_date()
        return\
            entry.store.active\
            and (vobj.get_Status() not in self.__e_closed)\
            and (due is not None)\
            and (due == _tomorrow)


class TodoStoreModel(StoreModel):
    item_cls = TodoStore

    def __init__(self, entries: TodoModel, *args, **kwargs):
        super().__init__(entries, *args, **kwargs)
        self._set_group = SetGroup.ToDo
        self._data = store_list


todo_model = TodoModel()
store_model = TodoStoreModel(todo_model)
