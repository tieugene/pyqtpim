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
    for i in range(3):    # el.size
        e = el.item(i)
        inner = e._data
        print(f"==== {i}: {e._fname}: ====")
        for k, v in inner.contents.items():
            if isinstance(v, list):
                if len(v) == 1:
                    print(f"<{k}>: {v[0].value}")  # or inner.<key> (like inner.summary.value
                else:
                    print(f"{k}: {v}")
            else:
                print(f"{k}: {v.value}")

test_e()
