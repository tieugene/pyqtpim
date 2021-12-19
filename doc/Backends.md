# Backends

Comparision of SQL vs File-based ToDo backends

## File-based
- &oplus; Simple sync (vdirsync, rsync)
- &oplus; transparent storage
- &oplus; Required 1.5 sync: inmem<>local_src[<>remote_src]
- &omius; Sort/Filter by QSFPM only

## SQL
- &oplus; Fast sort/filter using SQL (if QSqlQueryModel)
- &oplus; including Categories
- &ominus; Requires 3+ sync (DB<>body<>inmem<>local/remote_src)
- &ominus; Requires special sync w/ source
- &ominus; Extra data (vobj body + columns)
