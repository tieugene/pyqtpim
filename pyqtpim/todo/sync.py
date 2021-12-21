import os
# import pprint
import sys
import uuid
from typing import Optional, Any

import vobject
from PySide2 import QtSql

from . import enums, query
from .data import VObjTodo


def eprint(s: Any):
    print(s, file=sys.stderr)


def load_vobj(stream) -> Optional[VObjTodo]:
    if ventry := vobject.readOne(stream):
        if ventry.name == 'VCALENDAR':
            if 'vtodo' in ventry.contents:
                return VObjTodo(ventry)
            else:
                eprint("VCALENDAR have no VTODO")
        else:
            eprint("It is not VCALENDAR")
    else:
        eprint("Cannot read vobject")


def load_my(store_id: int) -> dict[uuid.UUID, (int, bool, VObjTodo)]:
    retvalue = dict()
    q = QtSql.QSqlQuery(f"SELECT id, syn, body FROM entry WHERE store_id={store_id}")
    while q.next():
        if vobj := load_vobj(q.value(2)):
            retvalue[uuid.UUID(vobj.getUID())] = (q.value(0), q.value(1), vobj)
    return retvalue


def load_remote(store_id: int) -> (dict[uuid.UUID, (str, VObjTodo)], str):
    retvalue = dict()
    path = None
    q = QtSql.QSqlQuery(f"SELECT DISTINCT connection FROM store WHERE id={store_id}")
    if q.next():
        path = q.value(0)
        with os.scandir(path) as itr:
            for entry in itr:
                if not entry.is_file():
                    continue
                with open(entry.path, 'rt') as stream:
                    if vobj := load_vobj(stream):
                        retvalue[uuid.UUID(vobj.getUID())] = (entry.path, vobj)
    else:
        eprint(f"Cannot get path of {store_id}")
    return retvalue, path


def set_my(q_str: str, vobj: VObjTodo, store_id: int, esyn: enums.ESyn) -> QtSql.QSqlQuery:
    q = QtSql.QSqlQuery()
    q.prepare(q_str)
    q.bindValue(':store_id', store_id)
    q.bindValue(':created', vobj.getCreated())
    q.bindValue(':dtstamp', vobj.getDTStamp())
    q.bindValue(':modified', vobj.getLastModified())
    q.bindValue(':dtstart', vobj.getDTStart())
    q.bindValue(':due', vobj.getDue())
    q.bindValue(':completed', vobj.getCompleted())
    q.bindValue(':progress', vobj.getPercent())
    q.bindValue(':priority', vobj.getPriority())
    q.bindValue(':status', vobj.getStatus())
    q.bindValue(':summary', vobj.getSummary())
    q.bindValue(':location', vobj.getLocation())
    q.bindValue(':syn', esyn.value)
    q.bindValue(':body', vobj.serialize())
    return q


def add_my(vobj: VObjTodo, store_id: int, esyn: enums.ESyn) -> bool:
    q = set_my(query.entry_add, vobj, store_id, esyn)
    return q.exec_()


def upd_my(entry_id: int, vobj: VObjTodo, store_id: int, esyn: enums.ESyn) -> bool:
    q = set_my(query.entry_upd, vobj, store_id, esyn)
    q.bindValue(':id', entry_id)
    return q.exec_()


def Sync(store_id: int, dry_run=True):
    """Standalone syncer DB<>source"""
    my_side: dict[uuid.UUID, (int, bool, VObjTodo)]
    remote_side: dict[uuid.UUID, (str, VObjTodo)]
    # 1. load all entry[store_id] into dict[uid: (id, body)]
    if not (my_side := load_my(store_id)):
        eprint("My side is empty")
        return
    # pprint.pprint(my_side)
    # 2. load all from connections into [uid: (path, body)]
    r_side, r_path = load_remote(store_id)
    if not (r_side and r_path):
        eprint("Remote side is empty")
        return
    # pprint.pprint(remote_side)
    # 3. Compare
    for uid, (my_id, my_syn, my_vobj) in my_side.items():
        # print(uid, my_id, my_syn, my_vobj.getSummary())
        if r_tuple := r_side.get(uid):  # both exist
            if my_syn == enums.ESyn.New.value:
                eprint(f"Impossible - both new: {uid} {my_vobj.getSummary()}")
                del r_side[uid]
            elif my_syn == enums.ESyn.Del.value:  # R-
                if dry_run:
                    print(f"R-: {uid} {my_vobj.getSummary()}")
                    del r_side[uid]
                    continue
                os.remove(r_side[uid][0])
                del r_side[uid]
                if not QtSql.QSqlQuery(query.entry_del % my_id):
                    eprint(f"Something bad with L-: {uid} {my_vobj.getSummary()}")
                # TODO: del cached
            else:  # Synced => cmp last-modified
                r_path, r_obj = r_tuple
                l_modified = my_vobj.getLastModified()
                r_modified = r_obj.getLastModified()
                if l_modified < r_modified:  # L<R
                    if dry_run:
                        print(f"L<R: {uid} {my_vobj.getSummary()}")
                        del r_side[uid]
                        continue
                    if not upd_my(my_id, r_obj, store_id, enums.ESyn.Synced):
                        eprint(f"Something bad with L<R: {uid} {r_obj.getSummary()}")
                elif l_modified > r_modified:  # L>R
                    if dry_run:
                        print(f"L>R: {uid} {my_vobj.getSummary()}")
                        del r_side[uid]
                        continue
                    data = my_vobj.serialize()
                    with open(r_path, 'wt') as o_f:
                        o_f.write(data)
                else:  # L==R; TODO: cmp whole of vobjs
                    pass
                del r_side[uid]  # processed
        else:  # my side only
            if my_syn == enums.ESyn.New.value:    # 3.1. L- => L>R
                if dry_run:
                    print(f"R+: {uid} {my_vobj.getSummary()}")
                    continue
                data = my_vobj.seriailze()
                with open(os.path.join(r_path, str(uid)+'.ics'), 'wt') as o_f:
                    o_f.write(data)
                    if not QtSql.QSqlQuery(query.entry_set_syn % (enums.ESyn.Synced.value, my_id)):
                        eprint(f"Something bad with R+: {uid} {my_vobj.getSummary()}")
            else:    # Del, Synced == 3.2. R-[L-] => L-
                if dry_run:
                    print(f"L-: {uid} {my_vobj.getSummary()}")
                    continue
                else:
                    if not QtSql.QSqlQuery(query.entry_del % my_id):
                        eprint(f"Something bad with L-: {uid} {my_vobj.getSummary()}")
                    # TODO: del cached
    # 3.3. Add L<R
    for uid, (path, vobj) in r_side.items():
        if dry_run:
            print(f"L+: {uid} {vobj.getSummary()}")
            continue
        if not add_my(vobj, store_id, enums.ESyn.Synced):
            eprint(f"Something bad with L+: {uid} {vobj.getSummary()}")
