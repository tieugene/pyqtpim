# ToDo

## 0. Now
- [ ] Learn @classmethod

### 0.1. Hot
*None*

### 0.2. Bugs
*None*

### 0.3. Issues
- [ ] TodoListView:
  - [ ] handle TodoView after selection out (entryDel, filter)

### 0.4. Features
- [ ] Settings save/restore:
  - [ ] sort
  - [ ] filter
  - [ ] column widths
- [ ] Prio: x5
- [ ] `import vobject` exact in `*/data.py` (-forms (tzutc()))
- [ ] Filter: f(unpacked vobj)
- [ ] Sort: f(unpacked vobjs)

### 0.5. UI/UX
- [ ] TodoForm:
  - [ ] Save previous selected store for .exec_new()
  - [ ] Shrink widget groups
  - [ ] Categories: special combobox (as RTM/Evolution)
  - [ ] Hide/Show optional fields (e.g. '>-- dtstart --'):
- [ ] TodoView:
  - [ ] compact
  - [ ] autowidth
  - [ ] [URL](URL)
  - [ ] Status: str
  - [ ] Prio: orig
- [ ] TodoListView:
  - [ ] Header tooltips
  - [ ] Show currently show tasks
  - [ ] Color `due today` (yellow) and `overdue` (red)
  - [ ] Expandable 'View File' messagebox
- [ ] StoreListView: auto-h/w

## 1. Common
- [ ] Docs:
  - [ ] docstrings
  - [ ] component diagram (UML)
  - [ ] compare PIMs

## 2. ToDo
- [ ] Categories
- [ ] Move entries between stores
- [x] LCRUD[^2]
- [ ] TodoForm: interim logic:
  - [ ] Summary != empty
  - [ ] Status & Completed & Progress
- [ ] Extend:
  - [ ] RRule
  - [ ] Alarm
  - [ ] multivalues[^4]:
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

## 4. Next:
- [ ] delay/async load
- [ ] Instant settings
- [ ] Actions: Enable/Disable by context
- [ ] Deployment:
  - [ ] docstrings
  - [ ] pylint
  - [ ] tox.ini
  - [ ] setup.py
  - [ ] \*.spec
- [ ] E: description/notes format as markdown:
  - X-ALT-DESC;FMTTYPE=text/html:
  - DESCRIPTION;ALTREP=text/html:
- [ ] In-mem SQLite [link by object id]
- [ ] SQL and File as unified backend

## x. misc

### x.1. Try
- [python-vdir](https://github.com/pimutils/python-vdir)
- [ics-py](https://github.com/ics-py/ics-py/)
- [icalendar](https://github.com/collective/icalendar/)
- [Xandicos](https://github.com/jelmer/xandikos) (server)

### x.2. SQL
- [ ] Check uid on load()
- [ ] Filter fault after add/del entry (id==None)
- [ ] Start...stop sync msg
- [ ] ~~TodoProxyModel~~
  - [ ] Sort
  - [ ] Filters
- [ ] Strict SQLite tables
- [ ] SQLite indexes

[^2]: Lightning/radicale compatible; not drop data exist
[^3]: CardBook/radicale compatible; not drop data exist
[^4]: QLineEdit[]/QListView/QPlainTextEdit
