import os
# import pprint
import sys
import uuid
from typing import Optional, Any

import vobject
from PySide2 import QtSql

from .data import VObjTodo


def eprint(s: Any):
    print(s, file=sys.stderr)


def load_vobj(stream) -> Optional[VObjTodo]:
    if ventry := vobject.readOne(stream):
        if ventry.name == 'VCALENDAR':
            if 'vtodo' in ventry.contents:
                return VObjTodo(ventry)
            else:
                eprint("This VCALENDAR have no VTODO")
        else:
            eprint("It is not VCALENDAR")
    else:
        eprint("Cannot read vobject")


def load_my(store_id: int) -> dict[uuid.UUID, (bool, VObjTodo)]:
    retvalue = dict()
    q = QtSql.QSqlQuery(f"SELECT id, syn, body FROM entry WHERE store_id={store_id}")
    while q.next():
        if vobj := load_vobj(q.value(2)):
            retvalue[uuid.UUID(vobj.getUID())] = (bool(q.value(1)), vobj)
    return retvalue


def load_remote(store_id: int) -> (dict[uuid.UUID, (str, VObjTodo)], str):
    retvalue = dict()
    path = None
    q = QtSql.QSqlQuery("SELECT connection FROM store WHERE id=%d" % store_id)
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


def Sync(store_id: int, dry_run=True):
    """Standalone syncer DB<>source"""
    my_side: dict[uuid.UUID, (bool, VObjTodo)]
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
    for my_uid, (my_syn, my_vobj) in my_side.items():
        print(my_uid, my_syn, my_vobj.getSummary())
        if my_uid not in r_side:    # L_new
            # 3.1. Del L>R
            # 3.2. Add L>R
            if dry_run:
                print(f"L>R: {my_uid}: {my_vobj.getSummary()}")
            else:
                data = my_vobj.seriailze()
                with open(os.path.join(r_path, str(my_uid)+'.ics'), 'wt') as o_f:
                    o_f.write(data)
        else:
            ...
    # 3.3. Add L<R
