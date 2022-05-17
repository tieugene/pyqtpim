# ToDo

## 0. Now

- Split into parts:
  - UI-independent (but vcalendar)
  - UI-specific (Qt, Web)

### 0.1. Hot (&rArr; release)
- [ ] TodoStoreListView: Auto-h/w  
   *(?QSplitter.setStretchFactor)*
- [ ] TodoView: Autowidth
- [ ] Settings save/restore:
  - [ ] MainWindow size
  - [ ] column widths (?)
- [ ] TodoForm:
  - [ ] Compact
  - [ ] On-the-fly logic (Status & Completed & Progress)
  - [ ] Validator (Summary != empty etc)

### 0.2. Bugs
*None*

### 0.3. Issues
- [ ] TodoListView.proxy: rowCount() lies
- [ ] QLable(URL): not works `goto`, `^C`

### 0.4. Features
- [ ] Description;AltRep="data:text/html,...":...

### 0.5. UI/UX
- [ ] Filter: +Upcoming
- [ ] Datetime fields: monofont (FontRole)
- [ ] TodoForm:
  - [ ] Hide/Show optional fields (e.g. '>-- dtstart --'):
  - [ ] Categories: special combobox (as RTM/Evolution)
- [ ] TodoView:
  - [ ] Status: str or w/ tooltip/statustip
  - [ ] Prio: +original value
  - [ ] URL as [URL](URL)
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
- [ ] Settings save/restore:
  - [ ] sort
  - [ ] filter

### 0.6. Inside
- [ ] Remove columns: Created/DTStamp/Modified/
- [ ] Filter: f(unpacked vobj)
- [ ] Sort: f(unpacked vobjs)
- [ ] `import vobject` exact in `*/data.py` (-forms (tzutc()))
- [ ] Use @classmethod

## 1. Common
- [ ] Docs:
  - [ ] docstrings
  - [ ] component diagram (UML)
  - [ ] compare PIMs

## 2. ToDo
- [ ] Categories
- [ ] Move entries between stores
- [x] LCRUD[^1]
- [ ] Extend:
  - [ ] RRule:
     - PIM generates virtual tasks from last 'Complete' up to tomorrow
     - Checking them adds 'Completed' tasks into this *.ics
     - Deleting completed tasks adds 'EXDATE:&lt;due&gt;' for completed and deleted tasks
  - [ ] Alarm
  - [ ] multivalues[^3]:
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

## 3. Journal

## 4. Calendar

## 5. Contacts
- [ ] LCRUD[^2]

## 6. Next
- [ ] i18n &rArr; l10n
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
- [python-vdir](https://github.com/pimutils/python-vdir) - Tools to read and write from/to
- [ics-py](https://github.com/ics-py/ics-py/) - iCalendar library
- [icalendar](https://github.com/collective/icalendar/) -  parser/generator for iCalendar files
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

[^1]: Lightning/radicale compatible; not drop data exist
[^2]: CardBook/radicale compatible; not drop data exist
[^3]: QLineEdit[]/QListView/QPlainTextEdit
