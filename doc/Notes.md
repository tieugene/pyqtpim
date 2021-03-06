# Notes
&check;
## Tips
- [CheckBox in QListView using QSqlTableModel](https://stackoverflow.com/questions/48193325/checkbox-in-qlistview-using-qsqltablemodel)
- [PyQt Layouts](https://realpython.com/python-pyqt-layout/)
- [Программирование на PyQt5 (43) - использование БД](https://russianblogs.com/article/36811088928/)
- [PyQt5 DB programming — CUD](https://developpaper.com/pyqt5-database-programming-adding-deleting-and-modifying-examples/)
- [Simple Todo](https://www.pythonguis.com/tutorials/modelview-architecture/)
- QSFPM:
  - [Custom QSFPM example](https://doc.qt.io/qt-5/qtwidgets-itemviews-customsortfiltermodel-example.html)
  - [Sorting and filtering table data with QSFPM](https://www.walletfox.com/course/qsortfilterproxymodelexample.php)
  - [Сортировка и фильтрация ... через Custom QSFPM](https://evileg.com/en/forum/topic/1421/)
  - [RTFM2](https://pretagteam.com/question/sort-by-multiple-columns-in-pyqt-model)
  - [RTFM1](https://github.com/dimkanovikov/MultisortTableView)

## RTFM:
- Sync:
  - [vdirsyncer](https://github.com/pimutils/vdirsyncer)
  - [CalDAV](https://pypi.org/project/caldav/) (CalDAV client)
  - [pyCardDAV](https://pypi.org/project/pyCardDAV/) (CardDAV CLI)
  - [~~SyncML~~](https://pypi.org/project/pysyncml/)
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

## misc
- classmethod: usual for cls.from_something(&hellip;) (alternate constructor | 'factory') for subclassing
- ListView ask model w/ DisplayRole; DetailsView - w/ EditRole
- Update VTODO:
  - componet.serialize() works fine - does not touch any exc. changed
  - but VTODO only; parent not available
  - => Todo(icalendar.vtodo) => Todo(icalendar)
- tz: can be for datetime and time
- Categories:
  - TB: csv in one property
  - Evolution: one cat per property
- Sync (ext):
  - nano `~/.config/vdirsync/config`
  - `vdirsyncer discover`
  - `vdirsyncer sync`
- QSqlRelationalTableModel: `store_id` changed to `name`, no one from `store_id`, `entry_store_id`, `entry_name_id`, `store_name_id` not works
- Update Todo record:
  - !form & !store: do nothing
  - !form &  store: just update store
  -  form & !store: update entry
  -  form &  store: save entry and store
- Form <> Rec+Entry <> File:
  - [x] New from Form:
    - new Obj
    - new Rec from Obj
  - [x] Upd from Form:
    - upd Obj
    - upd Rec from Form/Obj
  - [ ] New from File:
    - add Obj
    - new Rec from Obj
  - [ ] Upd from File:
    - repl Obj
    - upd all Rec from Obj
  - Operations:
    - new Obj from Form
    - upd Obj from Form
    - get Obj from File
    - new Rec from Obj
    - upd Rec from Obj | Form/Obj
- Datetimes:
  - current:
     - datetime.datetime.now() # 
     - datetime.datetime.now(timezone.utc) # UTC current time
     - datetime.datetime.utcnow() # naive
  - Timezone (`datetime.datetime.now().astimezone().tzname()`):

    ```python
    now: datetime = datetime.datetime.now()     # datetime.datetime naive
    local_now = now.astimezone()                # datetime.datetime w/ tz
    local_tz = local_now.tzinfo                 # datetime.tzinfo
    local_tzname = local_tz.tzname(local_now)   # str
    print(local_tzname)
    ```

- Datetimes:

    Name	| type	| VObj	| SQL	| Edit	| Show
    ------|---------|------|------|-----|------
    COMPLETED	| dt	| dtZ	| dtZ	| LocTime	| LocTime
    CREATED	| dt	| dtZ	| dtZ	| ---	| LocTime
    DTSTAMP	| dt	| dtZ	| ---	| ---	| LocTime
    DTSTART	| date	| date	| date	| date	| date
    	| dt	| dt[tz]	| dt[Z]	| dt[tz]	| LocTime
    DUE	| date	| date	| date	| date	| date
    	| dt	| dt[tz]	| dt[Z]	| dt[tz]	| LocTime
    LAST-M…D	| dt	| dtZ	| dtZ	| ---	| LocTime

- Sort (selectable, SQL):
  - id
  - Summary[>Due[>Prio]
  - Prio>Due>Summary
- Filters (Due|Status|Completed):
  - Active/Complete
  - All/Today/Tomorrow/Week
- Datetimes:
  - Created: like file ctime
  - DTStamp: special:  mtime w/o METHOD / ctime or special w/ METHOD
  - Last-Modified: like file mtime
- Sync:

 L | R | Case  | Act | Note
---|---|-------|-----|-----
 1 | 0 | L_new | L>R | +syn=2
 1 | 0 | R_del | L_x |
 0 | 1 | R_new | L<R | ---
 0 | 1 | L_del | R_x | store deleted
 1 | 1 | L_chg | L>R | ---
 1 | 1 | R_chg | L<R | ---
 1 | 1 | *_chg | ?win| ...

- get/set/del:
  - `var = property(get_var, set_var, del_var)`
  - `@property\ndef var(... | @var.setter\ndef var(...`

- set_X(v) -> bool:

   ```python
   def set_X(new):
     old = get_X()
     if new == old:
       return False
     if new == Any & old == None:
       vtodo.add('X').value = new
       return True
     if new == None & old != None:
       del vtodo['X']
       return True
     if new != None and old != None:
       vtodo.X.value = new  # but date/datetime: drop/add
     return True
  - test:
    - [x] .>N: F
    - [x] N>N: F
    - [x] N>A: T
    - [x] A>A: F
    - [x] A>B: T
    - [x] B>N: T
    - [ ] .>A: T

## vCard UML

- Property params:
  - PREF:1..100 - for any multivalue
  - TYPE: - FN, NICKNAME, PHOTO, ADR, TEL, EMAIL,
   IMPP, LANG, TZ, GEO, TITLE, ROLE, LOGO, ORG, RELATED, CATEGORIES, NOTE, SOUND, URL, KEY, FBURL, CALADRURI, CALURI

## Class/object relations

- `<|--`: Extension (Наследование) aka Generalization (Обобщение) - e.g. `Man <|-- Employee`
- `<-- `: Association (Ассоциация) - `1:*`
- `o-- `: Aggregation (Агрегация) == assoc:link; e.g. `container < item`
- `*-- `: Composition (Композиция) == aggreg:include; e.g. `list[]`
- `<|..`: Implementation (Реализация) - e.g. `class < i/f|abstract`
- `<.. `: Dependence (Зависимость) - weak link

## Cardinality:

RFC | Mean   | Re
----|--------|---
 1  | 1 must | 1
\*1 | 1 may  | ?
1\* | 1+ must| +
\*  | 1+ may | *

## Export .ics examples
- TBird - Task list - Export - \*.ics
- split into <uid>ics

## TBird ToDo:

### Hidden (8):

Type   | Field
-------|------
datime | CREATED
datime | LAST-MODIFIED
datime | DTSTAMP
uid    | UID
       | SEQUENCE
       | X-APPLE-SORT-ORDER
       | X-LIC-ERROR
       | X-MOZ-GENERATION

### Columns (9):

Name      | Type     | Field
----------|----------|------
Готово    | bool     | *STATUS:COMPLETED*
Важность  | enum     | PRIORITY
Название  | str      | SUMMARY
Начало    |date[time]| DTSTART
Срок      |date[time]| DUE
Продолжит.| interval | *virtual*
Выполнено | int      | PERCENT-COMPLETE
Завершено | datetime | COMPLETED
Категория | str      | CATEGORIES
Место     | str      | &hellip;
Состояние | enum     | STATUS
Календарь | str      | *virtual*

### Details (6)

Columns+

Name       | Type     | Field
-----------|----------|------
Повтор     | 
Напоминание|
Описание   | txt  | DESCRIPTION
Вложения   | ?    | ATTACH
Приватность| enum | CLASS

## vobject.icalendar.VTodo:
1. VTODO parameter <parm> can be accassable:
  - indirectly: obj.contents['parm'][0].value
  - directly: obj.parm.value
1. Return type: str (*see below*)
1. Exceptions:
  - not found the way to direct 'class' access
  - 'categories' is allways [str] or [[str]]
  - 'attach' can be as str as list

```python
knownChildren = {
    'DTSTART':        (0, 1, None),  # min, max, behaviorRegistry id
    'CLASS':          (0, 1, None),
    'COMPLETED':      (0, 1, None),
    'CREATED':        (0, 1, None),
    'DESCRIPTION':    (0, 1, None),
    'GEO':            (0, 1, None),
    'LAST-MODIFIED':  (0, 1, None),
    'LOCATION':       (0, 1, None),
    'ORGANIZER':      (0, 1, None),
    'PERCENT':        (0, 1, None),
    'PRIORITY':       (0, 1, None),
    'DTSTAMP':        (1, 1, None),
    'SEQUENCE':       (0, 1, None),
    'STATUS':         (0, 1, None),
    'SUMMARY':        (0, 1, None),
    'UID':            (0, 1, None),
    'URL':            (0, 1, None),
    'RECURRENCE-ID':  (0, 1, None),
    'DUE':            (0, 1, None),  # NOTE: Only one of Due or
    'DURATION':       (0, 1, None),  # Duration can appear
    'ATTACH':         (0, None, None),
    'ATTENDEE':       (0, None, None),
    'CATEGORIES':     (0, None, None),
    'COMMENT':        (0, None, None),
    'CONTACT':        (0, None, None),
    'EXDATE':         (0, None, None),
    'EXRULE':         (0, None, None),
    'REQUEST-STATUS': (0, None, None),
    'RELATED-TO':     (0, None, None),
    'RESOURCES':      (0, None, None),
    'RDATE':          (0, None, None),
    'RRULE':          (0, None, None),
    'VALARM':         (0, None, None)
}
```

## Date, Time:
- Date: 19970714
- Datime local: 19980118T230000
- Datime UTC: 19980119T070000Z
- Datime TZ: TZID=Europe/Moscow:19980119T020000

## Rsync
### Remote:
- `sudo dnf install rsync-daemon`
- `/etc/rsyncd.conf`:

  ```conf
  log file = /var/log/rsyncd.log
  uid = radicale
  gid = radicale
  use chroot = yes
  read only = yes
  # exclude = ".Radicale.*"

  [dav]
  path = /var/lib/radicale/collection-root/user

  ```

- `/etc/sysconfig/iptables`:

  ```iptables
  -A INPUT -s ... -p tcp -m state --state NEW -m tcp --dport 873 -j ACCEPT
  ```

### Local:

```bash
rsync -avz --del --exclude=".*" my.remote.host::dav .
```

[^4]: [Create GUI applications with Pyhon & Qt5 (PySide2 Edition)](https://www.pythonguis.com/pyside2-book/) &copy; Martin Fitzpatrick, $19/1295..14xx RUB, -35%?
