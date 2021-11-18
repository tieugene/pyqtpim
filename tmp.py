import os

from todo import Todo, TodoList, TodoListManager

indir = '_tmp/todo1'
infile = (
    os.path.join(indir, 'FFFFFFFF-FFFF-FFFF-FFFF-FFF413589559.ics'),
    os.path.join(indir, 'FFFFFFFF-FFFF-FFFF-FFFF-FFF413589749.ics'),
)


def test_elm():
    clm = TodoListManager()
    clm.itemAdd('AB', indir)
    # clm.reload()
    clm.print()


def test_el():
    cl = TodoList(indir)
    cl.print()


def test_e():
    el = TodoList('Test', indir)
    for i in range(el.size):    # el.size
        e = el.item(i)
        print(F"{i}: {e._fname}: {e._data.summary.value}")


test_e()
