"""Contact collections."""

# 1. std
import os
# 2. 3rd
# 3. local
from .entry import Contact


class ContactList(list[Contact]):
    """List of Contacts"""
    path: str

    def __init__(self, path: str = None):
        super().__init__()
        self.path = path

    @property
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
    """List of Lists of Contacts.
    :todo: use object instead of tuple
    """

    def __init__(self):
        super().__init__()

    @property
    def size(self):
        return len(self)

    def itemAdd(self, name: str, path: str):
        """Add new ContactList
        :param name: Associated name of ContactList
        :param path: Path to added ContactList
        :todo: collect=>path
        :todo: return something
        """
        cl = ContactList(path)
        cl.load()
        self.append((name, cl))

    def itemUpdate(self, i: int, name: str, path: str):
        old_entry = self[i]
        # TODO: process changing name/path/both
        cl = self[i][1]
        cl.clear()
        cl.path = path
        cl.load()
        self[i] = (name, cl)

    def itemDel(self, i: int) -> bool:
        if 0 < i < self.size:
            self[i][1].clear()
            del self[i]
            return True
        return False

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

    def load(self):
        for _, c in self:
            c.load()

    def findByName(self, s: str, i: int) -> bool:
        """Find existent CL by name [excluding i-th entry]
        :return: True if found
        """
        for j, (v, _) in enumerate(self):
            if v == s and j != i:
                return True
        return False

    def findByPath(self, s: str, i: int) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        for j, (_, v) in enumerate(self):
            if v.path == s and j != i:
                return True
        return False
