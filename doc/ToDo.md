# ToDo

## Now

### Job
- Reuse:
  - [ ] Who:
    - [ ] Mgr
    - [ ] List
    - [x] Entry (Extensions)
  - [ ] How:
    - Extension
    - ~~Class Object~~ *(too pythonic)*
    - Replace model of object

### Fixme

### Tuning
- [ ] CLM.Model:
  - [ ] insertRows()
  - [ ] updateRows()
- [ ] split `contact/*` by `part/layer.py`:
  - card/{data,view)
  - ab/{data,model,view)
  - mgr/{data,model,view)

## Contacts
- [ ] CLM.View:
  - [ ] autoshrink v/h
- [ ] CL.View:
  - [ ] autoshrink v/h[^1]
- [ ] C:
  - [x] Data: mv load() back to CL (item+source)
  - [x] Model: QDataWidgetMapper()
  - [ ] View: extend
  - [ ] C~~R~~UD, Info (*CardBook/radicale compatible*; not drop data exist)

### Next:
- [ ] CLM:
  - [ ] Model:
    - [x] QStringListModel
    - [ ] *All* virtual list / checkboxes
    - [ ] ?Rescan
- [ ] CL:
  - [ ] Data: async load
  - [ ] Model: QStandardItemModel (?)
  - [ ] View:
    - [ ] Columns handle:
       - [ ] select (== show/hide)
       - [ ] sort by
       - [ ] order
- [ ] C: &hellip;

## ToDo
(*Lightning/radicale compatible*)

## Calendar

## Journal

## misc

### RTFM
- [Create GUI applications with Pyhon & Qt5 (PySide2 Edition)](https://www.pythonguis.com/pyside2-book/) &copy; Martin Fitzpatrick, $19/1295..14xx RUB, -35%?

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
