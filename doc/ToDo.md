# ToDo

## 0. Now

### 0.1. Job
- [ ] E: Show raw content (html dt/dd | markdown):
  - Note #1: handle multiline strings (description)
  - Note #2: handle multivalues (categories, attach)
- [ ] ToDo: extend (columns(9))

### 0.2. Fixme
- [ ] Expandable 'View File' messagebox

### 0.3. Tuning
- [ ] ELM.Model:
  - [ ] insertRows()
  - [ ] updateRows()
- [ ] ELM.View: autoshrink v/h
- [ ] EL.View: autoshrink v/h[^1]
- [ ] Actions: Enable/Disable by context

## 1. Common

### 1.1. Next:
- [ ] ELM:
  - [ ] Model:
     - [x] QStringListModel
     - [ ] *All* virtual list / checkboxes
     - [ ] *Rescan*
- [ ] EL:
  - [ ] Data: async load
  - [ ] Model: QStandardItemModel (?)
  - [ ] View:
    - [ ] Columns:
       - [ ] on/off
       - [ ] sort by
       - [ ] order
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

## 2. Contacts
- [ ] C:
  - [ ] Extend
  - [ ] CRUD[^2]

## 3. ToDo
- [ ] C:
  - [ ] Extend
  - [ ] CRUD[^3]

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
