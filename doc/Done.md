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

## ToDo
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

## Contacts
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
