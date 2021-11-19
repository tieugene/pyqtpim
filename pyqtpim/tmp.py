import sys

from todo import TodoList, TodoListManager


def test_elm():
    clm = TodoListManager()
    clm.itemAdd('AB', sys.argv[1])
    # clm.reload()
    clm.print()


def test_el():
    cl = TodoList(sys.argv[1])
    cl.print()


def test_e():
    opt_fld = (
        'class',
        'completed',
        'dtstart',
        'due',
        'location',
        'percent-complete',
        'priority',
        'recurrence-id',
        'status',
        'summary'
    )

    def __print_one(k: str, v_list: list):
        if k != 'description':
            if len(v_list) == 1:
                v = v_list[0].value
                print(f"{k}: {v}")  # str; TODO: find .toNative()
            else:
                print(f"{k}: {v_list}")

    def __print1(item):
        """All possible"""
        keys = list(item.contents.keys())
        keys.sort()
        for k in keys:  # v: list allways
            __print_one(k, item.contents.get(k))

    def __print2(item):
        """All wanted"""
        for k in opt_fld:
            if v_list := item.contents.get(k):
                __print_one(k, v_list)

    def __print3(item):
        if 'attach' in item.contents:
            print(f"attach: {item.attach.value}")
        if 'categories' in item.contents:
            print(f"categories: {item.categories.value}")   # TODO: list only
        if 'class' in item.contents:
            print(f"class: {item.contents['class'][0].value}")  # TODO: as attribute
        if 'completed' in item.contents:
            print(f"completed: {item.completed.value}")
        if 'created' in item.contents:
            print(f"created: {item.created.value}")
        # DESCRIPTION (too big)
        print(f"dtstamp: {item.dtstamp.value}")
        if 'dtstart' in item.contents:
            print(f"dtstart: {item.dtstart.value}")
        if 'due' in item.contents:
            print(f"due: {item.due.value}")
        print(f"last-modified: {item.last_modified.value}")
        if 'location' in item.contents:
            print(f"location: {item.location.value}")
        if 'percent-complete' in item.contents:
            print(f"percent-complete: {item.percent_complete.value}")
        if 'priority' in item.contents:
            print(f"priority: {item.priority.value}")
        # TODO: RECURRENCE-ID
        if 'rrule' in item.contents:
            print(f"rrule: {item.rrule.value}")
        if 'sequence' in item.contents:
            print(f"sequence: {item.sequence.value}")
        if 'status' in item.contents:
            print(f"status: {item.status.value}")
        print(f"summary: {item.summary.value}")
        if 'transp' in item.contents:
            print(f"transp: {item.transp.value}")
        print(f"uid: {item.uid.value}")
        if 'url' in item.contents:
            print(f"url: {item.url.value}")
        if 'x-apple-sort-order' in item.contents:
            print(f"x-apple-sort-order: {item.x_apple_sort_order.value}")
        if 'x-lic-error' in item.contents:
            print(f"x-lic-error: {item.x_lic_error.value}")
        if 'x-moz-generation' in item.contents:
            print(f"x-moz-generation: {item.x_moz_generation.value}")

    el = TodoList('Test', sys.argv[1])
    for i in range(el.size):  # el.size
        e = el.item(i)
        inner = e._data
        print(f"==== {i}: {e._fname}: ====")
        __print3(inner)
        print()
    # TODO: print all keys found


test_e()
