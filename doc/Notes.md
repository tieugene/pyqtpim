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

