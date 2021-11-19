# Notes

## vCard UML

- Property params:
  - PREF:1..100 - for any multivalue
  - TYPE: - FN, NICKNAME, PHOTO, ADR, TEL, EMAIL,
   IMPP, LANG, TZ, GEO, TITLE, ROLE, LOGO, ORG, RELATED, CATEGORIES, NOTE, SOUND, URL, KEY, FBURL, CALADRURI, CALURI

## Class/object relations

En          | Ru          | Sign  | Mean | Example
------------|-------------|-------|-----|---
Extension   | Наследование | `<|--`| vs Generalization/Обобщение | `Man <|-- Employee`
Composition | Композиция   | `*--` | == aggreg:include | list[]
Aggregation | Агрегация    | `o--` | == assoc; :link | `container < item`
Association | Ассоциация   | `<--` | 1:*
Implementation | Реализация   | `<|..`| | `class < i/f|abstract`
Dependence | Зависимость  | `<..` |

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

### Datime examples:
DTSTART;TZID=Europe/Moscow:20210405T090000
COMPLETED:20210914T074957Z
