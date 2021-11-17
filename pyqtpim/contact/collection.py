"""Contact collections."""

# 2. 3rd
import vobject
# 3. local
from common import exc
from common.backend import EntryList, EntryListManager
from .entry import Contact


class ContactList(EntryList):
    def _load_one(self, fname: str, data: vobject.base.Component):
        if data.name == 'VCARD':
            self._data.append(Contact(fname, data))
        else:
            raise exc.EntryLoadError(f"It is not VCARD: {fname}")


class ContactListManager(EntryListManager):
    def itemAdd(self, name: str, path: str):
        self.append(ContactList(name, path))
