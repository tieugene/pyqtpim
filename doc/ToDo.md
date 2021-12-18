# ToDo

## 0. Now

### 0.0. Idea
- [ ] Back to file-based
  - [ ] QSFPM
  - [ ] All entries in one container

### 0.1. Job
- [ ] TodoList (proxy):
  - [ ] multifilter
- [ ] Sync

### 0.2. Fixme
- [ ] TodoForm:
  - [ ] rework/fix Prio edit
  - [ ] default tz - 'file...'
- [ ] TodoForm save errors:
  - [ ] C prio
  - [ ] U % (form:495)
- [ ] rollback on serialize() error (save())

### 0.3. Tuning
- [ ] Settings save/restore:
  - [ ] sort
  - [ ] filter
- [ ] 'Percent' => 'Progress'
- [ ] Shrink widget groups
- [ ] ELM.View: auto-h/w
- [ ] EL.View: auto-h/w[^1]
- [ ] Expandable 'View File' messagebox
- [ ] TodoForm.Categories: special combobox (as RTM/Evolution)

## 1. Common
- [ ] Docs:
  - [ ] docstrings
  - [ ] component diagram (UML)
  - [ ] compare PIMs
- [ ] 2-way sync
- [ ] EL: View:
  - [ ] sort
  - [ ] filter

## 2. ToDo
- [ ] Categories
- [ ] E:
  - […] Extend
  - […] CRUD[^2]
  - [ ] TodoForm: interim logic:
    - [ ] Summary != empty
    - [ ] Status & Completed & Progress
  - [ ] multivalues: (QLineEdit[]/QListView/QPlainTextEdit)
     - [ ] attach: (url)
     - [ ] comment: (str)
     - [ ] contact: (email/msgr/uuid)

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

