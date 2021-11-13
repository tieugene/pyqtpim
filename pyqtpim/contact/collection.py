"""Contact collections """

# 1. std
import os
# 2. 3rd
# 3. local
from .entry import Contact

ABs = []  # [('AB', '/Volumes/Trash/Documents/AB'),]


class ContactList(list[Contact]):
    """Contact list
    :todo: lazy/async [re]load
    """
    path: str

    def __init__(self, path: str = None):
        super().__init__()
        self.path = path

    def size(self):
        return len(self)

    def print(self):
        for v in self:
            v.print()

    def load(self):
        """Load entries from dir"""
        with os.scandir(self.path) as itr:
            for entry in itr:
                if not entry.is_file():
                    continue
                # TODO: chk mimetype
                self.append(Contact(entry.path))


class ContactListManager(list[(str, ContactList)]):

    def __init__(self):
        super().__init__()

    def size(self):
        return len(self)

    def add(self, name: str, collect: ContactList):
        self.append((name, collect))

    def print(self):
        for n, c in self:
            if c.size():
                print(f"==== {n} ====")
                c.print()
                print(f"==== /{n} ====")
            else:
                print(f"==== {n}/ ====")
        else:
            print("==== <empty> ====")

    def reload(self):
        for _, c in self:
            c.load()
