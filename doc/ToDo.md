# ToDo

## 0. Now

### 0.0. Idea
- [ ] Back to file-based:
  - [x] QAbstractTableModel ~~QStandardItemModel~~
  - [x] QSFPM
  - [x] All entries in one container (ist(Entry(store/body))
  - [ ] ? + in-mem SQLite
  - [ ] link by object id (like `uniq_ptr`)
- [ ] SQL and File as unified backend

### 0.1. Now
- [ ] TodoList:
  - [ ] decoration (color)
- [ ] Teach @classmethod

### 0.2. Bugs
- [ ] TodoView: Completed: tz
- [ ] TodoStore.active changed => refilter TodoListView
- [ ] TodoForm.exec_edit(): wrong Store
- [ ] TodoListView: bad refilter after entryDel()
- [ ] TodoListView: update/resort/refilter (?model) after:
  - [ ] entryEdit: update line + resort/refilter
  - [ ] entryDel: remove line
  - [ ] entryAdd: add line?

### 0.3. Issues
- [ ] TodoListView:
  - [ ] Autowidth
  - [ ] Autoheight
- [ ] TodoView:
  - [ ] Status: str
  - [ ] Prio: orig
- [ ] delay/async load

### 0.4. Features
- [ ] 'Percent' => 'Progress'
- [ ] Instant settings
- [ ] Settings save/restore:
  - [ ] sort
  - [ ] filter
  - [ ] column widths
- [ ] Prio: x5
- [ ] `import vobject` exact in `*/data.py`

### 0.5. UI/UX
- [ ] TodoForm:
  - [ ] Save previous selected store for (exec_new())
  - [ ] Shrink widget groups
  - [ ] Categories: special combobox (as RTM/Evolution)
  - [ ] Hide/Show optional fields (e.g. '>-- dtstart --'):
- [ ] TodoView:
  - [ ] compact
  - [ ] autowidth
  - [ ] URL as URL
- [ ] TodoListView:
  - [ ] Show currently show tasks
  - [ ] Color `due today` (yellow) and `overdue` (red)
  - [ ] auto-h/w[^1]
  - [ ] Expandable 'View File' messagebox
- [ ] StoreListView: auto-h/w

## 1. Common
- [ ] Docs:
  - [ ] docstrings
  - [ ] component diagram (UML)
  - [ ] compare PIMs
- [ ] 2-way sync
- [ ] EL: View:
  - [ ] sort
  - [ ] filter

### SQL
- [ ] Check uid on load()
- [ ] Filter fault after add/del entry (id==None)
- [ ] Start...stop sync msg
- [ ] ~~TodoProxyModel~~
  - [ ] Sort
  - [ ] Filters
- [ ] Strict SQLite tables
- [ ] SQLite indexes

## 2. ToDo

- [ ] Idea: VTodoObjExt[ended]: w/ store_id [and syn]
- [ ] Categories
- [ ] E:
  - [ ] Move synced between stores
  - […] Extend
  - […] CRUD[^2]
  - [ ] TodoForm: interim logic:
    - [ ] Summary != empty
    - [ ] Status & Completed & Progress
  - [ ] RRule
  - [ ] Alarm
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

