"""Contact collections """
import os
# 2. 3rd
# import magic # not works
import vobject
# 3. local
from .entry import Contact

# magic = magic.Magic()


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

    def load_f(self, fp: str):
        """Load entries from file
        :param fp: file path
        """
        # print(magic.from_file(fp))
        with open(fp, 'rt') as stream:
            for v in vobject.readComponents(stream):
                if v.name == 'VCARD':
                    self.append(Contact(v))

    def reload(self):
        """Load entries from dir"""
        with os.scandir(self.path) as itr:
            for entry in itr:
                if not entry.is_file():
                    continue
                self.load_f(entry.path)


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
            c.reload()
