# ToDo

## 0. Now

### 0.1. Job
- [ ] CU *(note: split logic & UI)*
  - [ ] save():
     - [ ] U:
       - [x] cmp
       - […] store
       - [ ] save (RTFM radicale, vobject tests)
     - [ ] C
  - [ ] interim logic
  - [ ] multivalues: multiline|checklist|stringlist:
     - [ ] attach (url): QLineEdit[]
     - [ ] categories: like RTM (editable combobox)
     - [ ] comment: QLineEdit[]
     - [ ] contact: like RTM
- [ ] D
- [ ] Docs: compare PIMs

### 0.2. Fixme
- [ ] TodoForm.CheckedDateTimeEdit[]: TZ
- [ ] Todo.Details:
  - [ ] extend (fields)
  - [ ] print `None`s
- [ ] TodoForm:
  - [ ] f_list
  - [ ] Date[Time]s: TZ

### 0.3. Tuning
- [ ] 'Percent' > 'Progress'
- [ ] ELM.View: auto-h/w
- [ ] EL.View: auto-h/w[^1]
- [ ] Expandable 'View File' messagebox (see QDialog.setSizeGripEnabled())

## 1. Common
- [ ] EL:
  - [ ] Data: sort
  - [ ] View: Columns:
     - [ ] on/off
     - [ ] sort by
     - [ ] order

### 1.1. Next:
- map models and mappers using str
- [ ] Find: how to control widgets after/with mapper? (QTextEdit resize, QDateTimeEdit time hide):
  - [ ] QDataWidgetMapper.currentIndexChanged(idx:int)+mappedWidgetAt()
  - [ ] QItemDelegate.paint(low-level paint)/.sizeHint(on resize only)
- [ ] Sync:
  - [ ] [SyncML](https://pypi.org/project/pysyncml/)
  - [ ] [CalDAV](https://pypi.org/project/caldav/)
  - [ ] [pyCardDAV](https://pypi.org/project/pyCardDAV/)
  - [ ] [](https://github.com/pimutils/vdirsyncer)
- [ ] Actions: Enable/Disable by context
- [ ] ELM:
  - [ ] Model:
     - [ ] insertRows()
     - [ ] updateRows()
     - [x] QStringListModel
     - [ ] *All* virtual list / checkboxes
- [ ] EL:
  - [ ] Data: async load
  - [ ] Model: QStandardItemModel (?)
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

## 2. ToDo
- [ ] E:
  - […] Extend
  - [ ] View: Show raw content (html dt/dd | markdown):
     - Note #1: handle multiline strings (description)
     - Note #2: handle multivalues (categories, attach)
  - [ ] CRUD[^2]
- [ ] EL: View: columnt delegates

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

## x. misc

### x.1. RTFM
- Try: [ics-py](https://github.com/ics-py/ics-py)
- Samples:
  - Mozilla Lightning
  - Apple Reminder
  - [Rainlendar2](http://www.rainlendar.net/) (&euro;5..10)
  - [Evolution](https://wiki.gnome.org/Apps/Evolution)
  - [OpenTasks](https://opentasks.app)
  - [RTM](https://www.rememberthemilk.com) ($40/y)
- [pimutils](https://github.com/pimutils)
- PySide2 Book[^4]
- Radicale src
- pyside2/examples:
  - tutorial/t8.py (UI)
  - widgets:
     - mainwindows/ (UI, mainwindow)
     - layouts/ (UI, layouts)
     - gallery/ (UI, widgets)
     - itemviews/addresbook/ (?)
     - tutorials/addressbook/ (CRUD)
  - sql/books/ (list/Details)

[^1]: self.horizontalHeader().setSectionResizeMode(model.fieldIndex("<fldName"), QHeaderView.ResizeToContents)
[^2]: Lightning/radicale compatible; not drop data exist
[^3]: CardBook/radicale compatible; not drop data exist
[^4]: [Create GUI applications with Pyhon & Qt5 (PySide2 Edition)](https://www.pythonguis.com/pyside2-book/) &copy; Martin Fitzpatrick, $19/1295..14xx RUB, -35%?
