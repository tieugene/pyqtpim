# Backends

Comparision of SQL vs File-based ToDo backends

## File-based
- &ominus; Sort/Filter by QSFPM only
- &oplus; 2x sync: inmem<>local_src[<>remote_src]
- &oplus; Simple sync (vdirsync, rsync)
- &oplus; transparent storage

## SQL
- &oplus; No proxy (if QSqlQueryModel)
- &oplus; Simple filter by Categories
- &ominus; 3x sync (DB<>body<>inmem<>local/remote_src)
- &ominus; Special sync w/ source
- &ominus; Extra data (vobj body + columns)
