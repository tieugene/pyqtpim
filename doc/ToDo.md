# ToDo

## Now

### Job

### Fixme

### Tuning
- [x] `__init__.py`: all-in-one
- [ ] code check:
  - [ ] built-in
  - [ ] flake8
  - [ ] pylint
- [ ] ELM.Model:
  - [ ] insertRows()
  - [ ] updateRows()

## Contacts
- [ ] CLM.View: autoshrink v/h
- [ ] CL.View: autoshrink v/h[^1]
- [ ] C:
  - [ ] Extend
  - [ ] C~~R~~UD, Info[^2]

### Next:
- [ ] CLM:
  - [ ] Model:
     - [x] QStringListModel
     - [ ] *All* virtual list / checkboxes
     - [ ] *Rescan*
- [ ] CL:
  - [ ] Data: async load
  - [ ] Model: QStandardItemModel (?)
  - [ ] View:
    - [ ] Columns handle:
       - [ ] on/off
       - [ ] sort by
       - [ ] order
- [ ] C: &hellip;

## ToDo
(*Lightning/radicale compatible*)

## Calendar

## Journal

## misc

### RTFM
- PySide2 Book[^3]

#### pyside2/examples
- tutorial/t8.py (UI)
- widgets:
  - mainwindows/ (UI, mainwindow)
  - layouts/ (UI, layouts)
  - gallery/ (UI, widgets)
  - itemviews/addresbook/ (?)
  - tutorials/addressbook/ (CRUD)
- sql/books/ (list/Details)

[^1]: self.horizontalHeader().setSectionResizeMode(model.fieldIndex("<fldName"), QHeaderView.ResizeToContents
[^2]: CardBook/radicale compatible; not drop data exist
[^3]: [Create GUI applications with Pyhon & Qt5 (PySide2 Edition)](https://www.pythonguis.com/pyside2-book/) &copy; Martin Fitzpatrick, $19/1295..14xx RUB, -35%?
