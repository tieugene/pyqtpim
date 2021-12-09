# ToDo

## 0. Now

### 0.0. Job
- Todo:
  - [ ] C
- Store:
  - [ ] listview => tableview
  - [ ] check on/off
  - [ ] set filter
  - [ ] 2-way sync (**del!**)
- TodoForm: .setValidator()
- Think:
  - all models - QSqlQueryModel
  - insert/update/delete using sql
  - db Entry repr class (`Entry.fld` against `record(i).value('fld')`)

### 0.1. Job-2
- [ ] List:
  - [ ] sort (1..4]
  - [ ] filter
  - [ ] columns on/off
  - [ ] columns order
- [ ] TodoForm: interim logic (on the fly; summary!)
- [ ] docstrings
- [ ] DTStart-link-Due = Duration?
- [ ] TodoForm: multivalues: (multiline|checklist|stringlist)
  - [ ] attach:  QLineEdit[] (url)
  - [ ] comment: QLineEdit[] (str)
  - [ ] contact: QLineEdit[] (email/msgr/uuid)
- [ ] TZ (on/off)
- [ ] Built-in sync (vdirsyncer.sync.sync())
- [ ] Docs: compare PIMs

### 0.2. Fixme
- [ ] UTC ('Z') datetime makes exception
- [ ] rollback on serialize() error (save())
- [ ] Todo.Completed: exact datetime[.utc]

### 0.3. Tuning
- [ ] TodoForm.Categories: special combobox (like RTM, Evolution)
- [ ] 'Percent' > 'Progress'
- [ ] ELM.View: auto-h/w
- [ ] EL.View: auto-h/w[^1]
- [ ] Expandable 'View File' messagebox (~~QDialog.setSizeGripEnabled()~~)

## 1. Common
- [ ] EL:
  - [ ] Data: sort
  - [ ] View:
     - [ ] sort
     - [ ] Columns:
        - [ ] on/off
        - [ ] order

### 1.1. Next:
- [ ] map models and mappers using str
- [ ] Find: how to control widgets after/with mapper? (QTextEdit resize, QDateTimeEdit time hide):
  - [ ] QDataWidgetMapper.currentIndexChanged(idx:int)+mappedWidgetAt()
  - [ ] QItemDelegate.paint(low-level paint)/.sizeHint(on resize only)
- [ ] Sync:
  - [ ] [vdirsyncer](https://github.com/pimutils/vdirsyncer)
  - [ ] [CalDAV](https://pypi.org/project/caldav/) (CalDAV client)
  - [ ] [pyCardDAV](https://pypi.org/project/pyCardDAV/) (CardDAV CLI)
  - [ ] [~~SyncML~~](https://pypi.org/project/pysyncml/)
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
  - […] CRUD[^2]
  - [ ] edit timezone
- [ ] EL: View: column delegates
- [ ] TodoForm: f_list

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

### x.2. Try
- [python-vdir](https://github.com/pimutils/python-vdir)
- [ics-py](https://github.com/ics-py/ics-py/)
- [icalendar](https://github.com/collective/icalendar/)
- [Xandicos](https://github.com/jelmer/xandikos) (server)

[^1]: self.horizontalHeader().setSectionResizeMode(model.fieldIndex("<fldName"), QHeaderView.ResizeToContents)
[^2]: Lightning/radicale compatible; not drop data exist
[^3]: CardBook/radicale compatible; not drop data exist
[^4]: [Create GUI applications with Pyhon & Qt5 (PySide2 Edition)](https://www.pythonguis.com/pyside2-book/) &copy; Martin Fitzpatrick, $19/1295..14xx RUB, -35%?
