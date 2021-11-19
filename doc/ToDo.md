# ToDo

## 0. Now

### 0.1. Job
- [ ] multivalues (categories, attach)
- [ ] Raw content
- [ ] handle datetime/date (dtstart, due)
- [ ] Test (and/or):
  - [ ] TBird w/ local dir
  - [ ] sync w/ remote
  - [ ] radicale@localhost

### 0.2. Fixme
- [ ] View.Class.text == status text
- [ ] Todo.Details: clear unused on change
- [ ] Todo.Details.Percent: 99 max

### 0.3. Tuning
- [ ] ELM.View: auto-h/w
- [ ] EL.View: auto-h/w[^1]
- [ ] Expandable 'View File' messagebox

## 1. Common
- [ ] EL:
  - [ ] Data: sort
  - [ ] View: Columns:
     - [ ] on/off
     - [ ] sort by
     - [ ] order

### 1.1. Next:
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
  - [ ] View: Show raw content (html dt/dd | markdown):
     - Note #1: handle multiline strings (description)
     - Note #2: handle multivalues (categories, attach)
  - [ ] Extend
  - [ ] CRUD[^3]

## 3. Contacts
- [ ] E:
  - [ ] Extend
  - [ ] CRUD[^2]

## x. misc

### x.1. RTFM
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
[^2]: CardBook/radicale compatible; not drop data exist
[^3]: Lightning/radicale compatible; not drop data exist
[^4]: [Create GUI applications with Pyhon & Qt5 (PySide2 Edition)](https://www.pythonguis.com/pyside2-book/) &copy; Martin Fitzpatrick, $19/1295..14xx RUB, -35%?
