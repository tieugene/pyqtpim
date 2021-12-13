# ToDo

## 0. Now

### 0.1. Job
- [ ] TodoList:
  - [ ] columns order:
     - [x] handly: QHeaderView.sectionMovable(); sectrionMoved()?
     - [ ] settings: QHeaderView.visualIndex() => list?
     - [ ] init: .swapSections()/.moveSection()
  - [ ] QSortFilterProxyModel:
     - [ ] multisort (e.g. default: prio=>due=>summary)
     - [ ] multifilter
- [ ] TodoForm: interim logic (on the fly, *summary*, .setValidator())
- [ ] docstrings
- [ ] DTStart-link-Due = Duration?
- [ ] TodoForm: multivalues: (multiline|checklist|stringlist)
  - [ ] attach:  QLineEdit[] (url)
  - [ ] comment: QLineEdit[] (str)
  - [ ] contact: QLineEdit[] (email/msgr/uuid)
- [ ] TZ (on/off)

### 0.2. Fixme
- [ ] UTC ('Z') datetime makes exception
- [ ] rollback on serialize() error (save())
- [ ] Todo.Completed: exact datetime[.utc]

### 0.3. Tuning
- [ ] TodoForm.Categories: special combobox (like RTM, Evolution)
- [ ] 'Percent' => 'Progress'
- [ ] ELM.View: auto-h/w
- [ ] EL.View: auto-h/w[^1]
- [ ] Expandable 'View File' messagebox (~~QDialog.setSizeGripEnabled()~~)
- [ ] Settings.col2show: wrap set into readable

## 1. Common
- [ ] Docs: compare PIMs
- [ ] 2-way sync
- [ ] EL:
  - [ ] Data: sort
  - [ ] View:
     - [ ] sort
     - [ ] Columns:
        - [ ] on/off
        - [ ] order

## 2. ToDo
- [ ] E:
  - […] Extend
  - […] CRUD[^2]
  - [ ] edit timezone
- [ ] EL: View: column delegates

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

## 4. Next:
- [ ] db Entry repr class (`Entry.fld` against `record(i).value('fld')`)
- [ ] DB:
  - [ ] QSqlTableModel => QSqlQueryModel
  - [ ] insert/update/delete using sql
- [ ] map models and mappers using str
- [ ] Find: how to control widgets after/with mapper? (QTextEdit resize, QDateTimeEdit time hide):
  - [ ] QDataWidgetMapper.currentIndexChanged(idx:int)+mappedWidgetAt()
  - [ ] QItemDelegate.paint(low-level paint)/.sizeHint(on resize only)
- [ ] Actions: Enable/Disable by context
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

## x. misc

### x.1. Try
- [python-vdir](https://github.com/pimutils/python-vdir)
- [ics-py](https://github.com/ics-py/ics-py/)
- [icalendar](https://github.com/collective/icalendar/)
- [Xandicos](https://github.com/jelmer/xandikos) (server)

[^1]: self.horizontalHeader().setSectionResizeMode(model.fieldIndex("<fldName"), QHeaderView.ResizeToContents)
[^2]: Lightning/radicale compatible; not drop data exist
[^3]: CardBook/radicale compatible; not drop data exist

