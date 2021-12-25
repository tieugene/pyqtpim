# Backends

Comparision of SQL vs File-based ToDo backends

## File-based
- &ominus; Sort/Filter by QSFPM only
- &oplus; 2x sync: mem>local>remote
- &oplus; Simple sync (vdirsync, rsync)
- &oplus; transparent storage

## SQL
- &oplus; No proxy (if QSqlQueryModel)
- &oplus; Simple filter by Categories
- &ominus; 3x sync (mem>DBx2>local>remote
- &ominus; Special sync w/ source
- &ominus; Extra data (vobj body + columns)
