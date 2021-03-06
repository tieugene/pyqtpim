# PIM comparision

- ToDo only
- User defined CalDAV server

## By one

### Want:
- Max RFC-5545 support:
  - Fileds: Status (4), Prio (4), Class (4), URL, Attach, Contact, Comment
  - DTStatart/Due: date | datetime
  - Subtasks/Linked
- Off-line
- Sync w/ self-hosted CalDAV (e.g. Radicale)
- List on/off (show/hide)
- Multisort (sort on multiple columns)
- Filters: ...
- Description: plain/md/html

### [RTM](https://www.rememberthemilk.com)
- &odot; RAM=200MB (Linux)
- &odot; Subtasks (Pro)
- &ominus; Pro = $40/y
- &ominus; ~~Off-line~~ (Pro only) &rArr; *нет инета - нет todo*
- &ominus; ~~Self CebDAV~~
- &ominus; ~~Attaches~~ (Pro - GDrive/Dropbox/MyComp)
- &ominus; ~~Multifilter~~ (e.g. Today & List1 & Cat1)
- &ominus; ~~List on/off~~
- &ominus; Status: Active/Done (maybe 'in progress')
- &ominus; Touch-oriented UI

### Lightning
- &ominus; DTStart/Due - datetime only
- &ominus; ~~Filters~~ (work strange)
- &ominus; Prio: `Normal` looks like `None`
- &ominus; Fields: URL (r/o), ~~Comments~~, ~~Contact~~
- &ominus; Permanent buggy
- &ominus; ~~Multisort~~
- &ominus; Cancelled are active

Why not: ~~Filter~~, ~~Multisort~~, ~~Due:date~~, ~~URL~~

### [Rainlendar2](http://www.rainlendar.net/)
- &ominus; (&euro;5..10)
- &ominus; Buy via PayPal only
- &ominus; Bug: Cannot Status=None
- &ominus; Strange 'Sensivity' field ('Class'?)
- &ominus; System-wide modal windows
- &ominus; страшный шоппц

Why not: ~~Status=None~~

### [Evolution](https://wiki.gnome.org/Apps/Evolution)
- &oplus; DTStart/Due date/datetime
- &oplus; Custom sort
- &ominus; Громоздкие *.ics
- &ominus; innormous uid
- &ominus; DTStart/Due date/datetime both only
- &ominus; ~~Class=None~~
- &ominus; Wide `Prio`
- &ominus; Attach: files only
- &ominus; Нет "Все задачи"
- &ominus; Нет "Today"

Why not: Linux only

### [OpenTasks](https://opentasks.app)
- &ominus; Cannot Status=None (bug [#807](https://github.com/dmfs/opentasks/issues/807))
- &oplus; Subtasks?

Why not: Status=~~None~~Need-Action

### Apple Reminder

## Alltogether

### Fields

## Android:
- [x] OpenTasks: Need-Actions
- [x] ~~Мои Дела~~ (My Tasks): unmovable, ничего нет
- [x] ~~Мой Ежедневник~~ 1.8.1.2 (): ~~CalDAV~~
- [x] ~~Tasks~~ (): ~~CalDAV~~
- [x] ~~To-do~~ List (): глючная хрень
- [x] ~~Список задач~~ (Splend Apps): unmovable, ~~CalDAV~~
- [x] ~~OpenSync~~ unmovable
- […] CalDAV TaskSync: nice &hellip;, but unmaintained
- […] DavX5: слетают настройки после каждого обновления
- [x] ~~CalendarSync~~: cannot connect
- [x] ~~aCalendar~~: (Tapir Apps): CalDAV not found
- [x] ~~Простой календарь~~: CalDAV settings not found, Calendar (not todolist)
