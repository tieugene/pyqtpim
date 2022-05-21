"""PySide interface"""

# 1. system
# 2. PySide
# 3. local
from base import SetGroup, EntryModel, StoreModel
from core.contact.data import ContactList, ContactStoreList
from core.contact import enums


class ContactModel(EntryModel):
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


class ContactListManagerModel(StoreModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_group = SetGroup.Contacts
        self._data = ContactStoreList()
        # self._init_data()
