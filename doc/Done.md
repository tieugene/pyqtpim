# Done

## All
- [x] MySettings
- [x] Raw content (plain/md/html/richtext)
- [x] Test: sync w/ remote
- [ ] control widgets after/with mapper:
  - [x] ~~QDateTimeEdit.dateChanged()/timeChanged()/dateTimeChanged()~~:
    - On None or not changed: does nothing
    - On datime: DateTime > Date > Time; after Date - Date only (00:00:00 not changed)
    - On date: DateTime > Date (time = 00:00:00)
  - [x] ~~QDateTimeEdit: inherit + replace setDate/setTime/setDateTime~~ - no effect
- [x] GroupDAV sync (ext)

### Todo
- [x] 1-way sync:
  - [x] date[times]: str iso 8601 (date[time].isoformat()/fromisoformat(); 
  - [x] body: db
  - [x] ~~vcal cache~~: dict[id, vcal]
- [x] ~~QSqlRelTablrModel~~ bad idea
- [x] Todo:
  - [x] U (+f_list)
  - [x] D
  - [x] C
- [x] Store:
  - [x] active: check on/off
  - [x] set filter
- [x] Remove unwanted (file-based)
- [x] TodoList: columns on/off
- [x] TodoList: column order
- [x] ~~DTStart-link-Due (TB) => Duration?~~ No
- [x] Todo.reloadColOrder() algo



## Contacts.File-based
- [ ] CLM:
  - [x] CRUD, Info
  - [x] Hidden inner data
- [ ] CL:
  - [ ] CRUD:
    - [ ] C
    - [x] R
    - [ ] U
    - [ ] D
  - [x] Load on demand
  - [x] Hidden inner data
- [ ] C:
  - [x] Hidden inner data

## ToDo.File-based
- [x] Test:
  - [x] ~~Find: TB Ligtning extension for todo in localdir~~
  - [x] ~~Lightning todo w/ local dir (`file:///`)~~
  - [x] rsync
- [x] Details.Percent: 99>100% max
- [x] multivalues:
  - [x] categories: list: csv, detail: multiline text
- [x] Column: name:str => enum (ListModel._fld_names, data/Entry._name2func)
- [x] ListView: hide extra columns (xListView.__init__(): .setColumnHidden(...))
- [x] Expand fields:
  - [x] Data
  - [x] List
  - [x] Details
- [x] Details: RTF text
- [x] multivalues: list: csv, details: UL
- [x] Details: handle datetime/date (dtstart, due):
- [x] CUD:
  - [x] fields
  - [x] load (U):
     - [x] Categories: CSV
     - [x] QDate[Time]Edit: checked pairs
     - [x] prio,progress: slider+spinbox
     - [x] class/status: w/ 'none'
  - [x] cmp
  - [x] store
  - [x] save (+sequence, +lastmodified)
  - [x] D[el]
  - [x] C[reate]
- [x] TodoForm.CheckedDateTimeEdit[]: TZ (datetime only)
- [x] Todo.Details: extended (12 fields)
- [x] Todo.Details: print `None`s
- [x] Something wrong with cats
- [x] LastModified: add 'Z'
