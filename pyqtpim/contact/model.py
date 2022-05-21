"""PySide interface"""

# 1. system
# 2. PySide
# 3. local
from base import SetGroup, EntryModel, StoreModel
from pym_core.contact.data import ContactList, ContactStoreList
from pym_core.contact import enums as core_enums


class ContactModel(EntryModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = ContactList()
        self._fld_names = (
            (core_enums.EProp.FN, "FN"),
            (core_enums.EProp.Family, "Last name"),
            (core_enums.EProp.Name, "First name"),
            (core_enums.EProp.Email, "Email"),
            (core_enums.EProp.Phone, "Tel.")
        )

    def _empty_item(self) -> ContactList:
        return ContactList()


class ContactListManagerModel(StoreModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.Contacts
        self._data = ContactStoreList()
        # self._init_data()
