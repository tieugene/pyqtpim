"""Contact collections """

# 1. std
import os
# 2. 3rd
# 3. local
from .entry import Contact

ABs = []  # [('AB', '/Volumes/Trash/Documents/AB'),]


class ContactList(list[Contact]):
    """List of Contacts"""
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
    """List of Lists of Contacts"""

    def __init__(self):
        super().__init__()

    # TODO: @property
    def size(self):
        return len(self)

    def add(self, name: str, collect: ContactList):
        """Add new ContactList
        :param name: Associated name of ContactList
        :param collect: ContactList to add
        :todo: return something
        """
        self.append((name, collect))

    def rm_by_idx(self, i: int) -> bool:
        if 0 < i < self.size():
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

    def findByName(self, s: str) -> bool:
        """Find existent CL by name
        :return: True if found
        """
        for v, _ in self:
            if v == s:
                return True
        return False

    def findByPath(self, s: str) -> bool:
        """Find existent CL by name
        :return: True if found
        """
        for _, v in self:
            if v.path == s:
                return True
        return False
