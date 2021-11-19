"""PySide interface"""

# 1. system
# 2. PySide
from PySide2 import QtCore
# 3. local
from common import SetGroup, EntryListModel, EntryListManagerModel
from .data import ContactList, ContactListManager


class ContactListModel(EntryListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = ContactList()
        self._fld_names = (
            ("FN", 'fn'),
            ("Last name", 'family'),
            ("First name", 'given'),
            ("Email", 'email'),
            ("Tel.", 'tel')
        )

    def _empty_item(self) -> ContactList:
        return ContactList()


class ContactListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.Contacts
        self._data = ContactListManager()
        self._init_data()
