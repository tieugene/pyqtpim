"""Contact collections."""

# 1. std
import os
# 2. 3rd
# 3. local
from .entry import Contact


class ContactList(object):
    """List of Contacts"""
    __path: str
    __name: str
    __data: list[Contact]
    __ready: bool

    def __init__(self, name: str = None, path: str = None):
        super().__init__()
        self.__name = name
        self.__path = path
        self.__data = []
        self.__ready = False

    def __load(self):
        """Load entries from dir"""
        if self.__path:
            # print(f"{self.__name}: Loading from {self.__path}")
            with os.scandir(self.__path) as itr:
                for entry in itr:
                    if not entry.is_file():
                        continue
                    # TODO: chk mimetype
                    self.__data.append(Contact(entry.path))

    def __chk_ready(self):
        if not self.__ready:
            self.__load()
            self.__ready = True

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def size(self):
        self.__chk_ready()
        return len(self.__data)

    def print(self):
        self.__chk_ready()
        for v in self.__data:
            v.print()

    def item(self, i: int) -> Contact:
        """Get list item"""
        self.__chk_ready()
        return self.__data[i]

    def update(self, name: str, path: str):
        self.__name = name
        if path != self.__path:
            self.__data.clear()
            self.__path = path
            self.__ready = False


class ContactListManager(list[ContactList]):
    """List of Lists of Contacts."""

    def __init__(self):
        super().__init__()

    @property
    def size(self):
        return len(self)

    def itemAdd(self, name: str, path: str):
        """Add new ContactList
        :param name: Associated name of ContactList
        :param path: Path to added ContactList
        :todo: return something
        """
        self.append(ContactList(name, path))

    def itemUpdate(self, i: int, name: str, path: str):
        # old_entry = self[i]
        self[i].update(name, path)

    def itemDel(self, i: int) -> bool:
        if 0 < i < self.size:
            del self[i]
            return True
        return False

    def print(self):
        for n, cl in self:
            cl.print()

    def findByName(self, s: str, i: int) -> bool:
        """Find existent CL by name [excluding i-th entry]
        :return: True if found
        """
        for j, cl in enumerate(self):
            if cl.name == s and j != i:
                return True
        return False

    def findByPath(self, s: str, i: int) -> bool:
        """Find existent CL by path [excluding i-th entry]
        :return: True if found
        """
        for j, cl in enumerate(self):
            if cl.path == s and j != i:
                return True
        return False
