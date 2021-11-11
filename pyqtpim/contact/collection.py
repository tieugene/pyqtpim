"""Contact list"""
import os
# 2. 3rd
# import magic # not works
import vobject
# 3. local
from .entry import Contact

# magic = magic.Magic()


class ContactList(list):
    name: str
    path: str

    def __init__(self, name: str, path: str = None):
        self.name = name
        self.path = path

    def print(self):
        print(f"==== {self.name} ====")
        for v in self:
            v.print()
        print(f"==== /{self.name} ====")

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
