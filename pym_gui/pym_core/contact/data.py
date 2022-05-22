"""Contacts data provider

Most interesting (see contents:dict):
- fn:FN (card: 1): .fn.value
- n:N (card: ?): .n[...]:Name.value:dict.{family/given/additional}
- email:list(EMAIL) (card: ?)
- tel:list(TEL) (card: ?)
"""
# 2. 3rd
import vobject
# 3. local
from pym_core.base.data import VObj, EntryList, StoreList
from pym_core import exc
from . import enums


class Contact(VObj):
    """Contact itself"""
    def __init__(self, path: str, vcard: vobject.base.Component):
        super().__init__(path, vcard)
        self._name2func = {
            enums.EProp.FN: self.getFN,
            enums.EProp.Family: self.getFamily,
            enums.EProp.Name: self.getGiven,
            enums.EProp.Email: self.getEmailList,
            enums.EProp.Phone: self.getTelList
        }

    def print(self):
        def __fn():
            print(f"FN: {self._data.fn.value}")

        def __name():
            if n := self._data.contents.get('n'):
                print("N:", )
                v = n[0].value
                print(v.__dict__)
                # print(v.family)

        def __email():
            if email := self._data.contents.get('email'):
                print("Email:", )
                v = email[0]
                print(v.__dict__)
                print(f"value: {v.value}")
                if pref := v.params.get('PREF'):
                    print(f"pref: {bool(pref[0])}")
                print(", ".join([v.value for v in email]))
        __fn()
        __name()
        __email()

    def getFN(self) -> str:
        return self._data.fn.value

    def getFamily(self) -> str:
        if n := self._data.contents.get('n'):
            return n[0].value.family
        return ''

    def getGiven(self) -> str:
        if n := self._data.contents.get('n'):
            return n[0].value.given
        return ''

    def getEmailList(self) -> str:
        """:todo: preferable or list"""
        if email := self._data.contents.get('email'):
            return ", ".join([v.value for v in email])
        return ''

    def getTelList(self) -> str:
        """:todo: preferable or list"""
        if tel := self._data.contents.get('tel'):
            return ", ".join([v.value for v in tel])
        return ''


class ContactList(EntryList):
    def _load_one(self, fpath: str, data: vobject.base.Component):
        if data.name == 'VCARD':
            self._list.append(Contact(fpath, data))
        else:
            raise exc.EntryLoadError(f"It is not VCARD: {fpath}")


class ContactStoreList(StoreList):
    def itemAdd(self, name: str, path: str):
        self.append(ContactList(name, path))
