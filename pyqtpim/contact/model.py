"""PySide interface"""

# 1. system
# 2. PySide
# 3. local
from common import SetGroup, EntryListModel, EntryListManagerModel
from .data import ContactList, ContactListManager
from . import enums


class ContactListModel(EntryListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = ContactList()
        self._fld_names = (
            (enums.EProp.FN, "FN"),
            (enums.EProp.Family, "Last name"),
            (enums.EProp.Name, "First name"),
            (enums.EProp.Email, "Email"),
            (enums.EProp.Phone, "Tel.")
        )

    def _empty_item(self) -> ContactList:
        return ContactList()


class ContactListManagerModel(EntryListManagerModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.Contacts
        self._data = ContactListManager()
        # self._init_data()
