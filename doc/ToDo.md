# ToDo

## 0. Now

### 0.1. Hot
- [ ] TodoListView:
  - [ ] Shorter dates: dd.mm[.yy][ hh:mm]
  - [ ] Due Color: red→orange→white|yellow→green→blue
  - [ ] Due Decorate: dd.mm→yest→2day→tomor→dd.mm
  - [ ] Autowidth: all excl. Summary/Location
- [ ] TodoView:
  - [ ] ru date[time]s: dd.mm.yy[ hh:mm]
  - [ ] Status: str
  - [ ] Prio: orig[+color]
  - [ ] [URL](URL)
  - [ ] autowidth
  - [ ] compact
- [ ] TodoForm:
  - [ ] Save previous selected store for .exec_new()
  - [ ] Shrink widget groups
- [ ] TodoStoreListView:
  - [ ] auto-h/w
- [ ] Settings save/restore:
  - [ ] sort
  - [ ] filter
  - [ ] column widths

### 0.2. Bugs
*None*

### 0.3. Issues
- [ ] TodoListView.proxy: statusbar counter lies
   *(? QtCore.Qt.StatusTipRole)*

### 0.4. Features
- [ ] Filter: f(unpacked vobj)
- [ ] Sort: f(unpacked vobjs)
- [ ] TodoForm: interim logic:
  - [ ] Summary != empty
  - [ ] Status & Completed & Progress
- [ ] `import vobject` exact in `*/data.py` (-forms (tzutc()))
- [ ] Use @classmethod
- [ ] Description;AltRep="data:text/html,...":...

### 0.5. UI/UX
- [ ] TodoForm:
  - [ ] Hide/Show optional fields (e.g. '>-- dtstart --'):
  - [ ] Categories: special combobox (as RTM/Evolution)
- [ ] TodoView:
  - [ ] ? Desc in tab
- [ ] TodoListView:
  - [ ] Hot buttons: chg:
     - [ ] Prio
     - [ ] Due
     - [ ] Store
     - [ ] Tags
  - [ ] Selection after:
     - entryAdd: to added entry if || prev
     - entryDel: &hellip;
     - entryEdit: to edited entry || &hellip;
  - [ ] Expandable 'View File' messagebox

## 1. Common
- [ ] Docs:
  - [ ] docstrings
  - [ ] component diagram (UML)
  - [ ] compare PIMs

## 2. ToDo
- [ ] Categories
- [ ] Move entries between stores
- [x] LCRUD[^2]
- [ ] Extend:
  - [ ] RRule
  - [ ] Alarm
  - [ ] multivalues[^4]:
     - [ ] attach: (url)
     - [ ] comment: (str)
     - [ ] contact: (email/msgr/uuid)
- [ ] Prio: x5

### RTM
- InstantAdd (+Inbox)
- Enums:
  - location
  - category ('tags')
- Add properties on demand

## 3. Contacts
- [ ] LCRUD[^3]

## 4. Next:
- [ ] delay/async load
- [ ] Instant settings
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
