# ToDo

## Now

### Job
- [ ] C: QDataWidgetMapper()

### Fixme

### Tuning
- [ ] split `contact/*` by `part/layer.py`:
  - card/{data,view)
  - ab/{data,model,view)
  - mgr/{data,model,view)
- Reuse Mgr/List/Details:
  - Inherit
  - Class Object
  - Replace model of object

## Contacts
- [ ] CLM.View:
  - [ ] self.model().selectionModel().selectionChanged => self.selectionModel().currentRowChanged()
  - [ ] autoshrink v/h
- [ ] CL.View:
  - [ ] self.model().selectionModel().selectionChanged => self.selectionModel().currentRowChanged()
  - [ ] autoshrink v/h
- [ ] C:
  - [ ] Data: mv load() back to CL (item+source)
  - [ ] Model: QDataWidgetMapper()
  - [ ] View: extend
  - [ ] C~~R~~UD, Info (*CardBook/radicale compatible*; not drop data exist)

### Next:
- [ ] CLM:
  - [ ] Model:
    - [ ] QStandardItemModel/QStringListModel
    - [ ] *All* virtual list / checkboxes
    - [ ] ?Rescan
- [ ] CL:
  - [ ] Data: async load
  - [ ] Model: QStandardItemModel (?)
  - [ ] View:
    - [ ] Columns handle:
       - [ ] sort by
       - [ ] select (== show/hide)
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
