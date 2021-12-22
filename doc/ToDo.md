# ToDo

## 0. Now

### 0.0. Idea
- [ ] SQL and File as unified backend
- [ ] Back to file-based:
  - [ ] or QStandardItemModel>QStandardItem
  - [ ] or QAbstractTableModel
  - [ ] QSFPM
  - [ ] All entries in one container:
    - _list(Entry(body, store_id)_
    - ~~list[store_id, Entry(body)]~~
    - ~~list[Entry]+dict[entry:store_id]~~
  - [ ] ? + in-mem SQLite

### 0.1. Job
- [ ] TodoList: QSqlQueryModel
  - [ ] ~C~RU~D~
  - [ ] Sort
  - [ ] Filters

### 0.2. Fixme (critical)

### 0.3. Fixme (soft)
- [ ] Check uid on Reload
- [ ] Strict SQLite tables
- [ ] Filter fault after add/del entry (id==None)
- [ ] TodoForm:
  - [ ] rework/fix Prio edit
  - [ ] default tz - 'file...'
- [ ] Store: QSqlQueryModel: RUD

### 0.4. Tuning
- [ ] Start...stop msg
- [ ] todo.data.VTodoObj.getX - @prop w/ decorator
- [ ] SQLite indexes
- [ ] Color `due today` (yellow) and `overdue` (red)
- [ ] Instant settings
- [ ] Settings save/restore:
  - [ ] sort
  - [ ] filter
- [ ] 'Percent' => 'Progress'
- [ ] Prio: x5
- [ ] Shrink widget groups
- [ ] ELM.View: auto-h/w
- [ ] EL.View: auto-h/w[^1]
- [ ] Expandable 'View File' messagebox
- [ ] TodoForm.Categories: special combobox (as RTM/Evolution)

## 1. Common
- [ ] Docs:
  - [ ] docstrings
  - [ ] component diagram (UML)
  - [ ] compare PIMs
- [ ] 2-way sync
- [ ] EL: View:
  - [ ] sort
  - [ ] filter

## 2. ToDo
- [ ] Categories
- [ ] E:
  - […] Extend
  - […] CRUD[^2]
  - [ ] TodoForm: interim logic:
    - [ ] Summary != empty
    - [ ] Status & Completed & Progress
  - [ ] multivalues: (QLineEdit[]/QListView/QPlainTextEdit)
     - [ ] attach: (url)
     - [ ] comment: (str)
     - [ ] contact: (email/msgr/uuid)

### RTM
- InstantAdd (+Inbox)
- Enums:
  - location
  - category ('tags')
- Add properties on demand

## 3. Contacts
- [ ] E:
  - [ ] Extend
  - [ ] CRUD[^3]

## 4. Next:
- [ ] db Entry repr class (`Entry.fld` against `record(i).value('fld')`)
- [ ] DB:
  - [ ] QSqlTableModel => QSqlQueryModel
  - [ ] insert/update/delete using sql
- [ ] map models and mappers using str
- [ ] Find: how to control widgets after/with mapper? (QTextEdit resize, QDateTimeEdit time hide):
  - [ ] QDataWidgetMapper.currentIndexChanged(idx:int)+mappedWidgetAt()
  - [ ] QItemDelegate.paint(low-level paint)/.sizeHint(on resize only)
- [ ] Actions: Enable/Disable by context
- [ ] E:
  - [ ] description/notes format as markdown:
     - X-ALT-DESC;FMTTYPE=text/html:
     - DESCRIPTION;ALTREP=text/html:
- [ ] Deployment:
  - [ ] docstrings
  - [ ] pylint
  - [ ] tox.ini
  - [ ] setup.py
  - [ ] \*.spec

## x. misc

### x.1. Try
- [python-vdir](https://github.com/pimutils/python-vdir)
- [ics-py](https://github.com/ics-py/ics-py/)
- [icalendar](https://github.com/collective/icalendar/)
- [Xandicos](https://github.com/jelmer/xandikos) (server)

[^1]: self.horizontalHeader().setSectionResizeMode(model.fieldIndex("<fldName"), QHeaderView.ResizeToContents)
[^2]: Lightning/radicale compatible; not drop data exist
[^3]: CardBook/radicale compatible; not drop data exist

