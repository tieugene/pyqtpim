"""Contact itself

Most interesting (see contents:dict):
- fn:FN (card: 1): .fn.value
- n:N (card: ?): .n[...]:Name.value:dict.{family/given/additional}
- email:list(EMAIL) (card: ?)
- tel:list(TEL) (card: ?)
"""

from common.backend import Entry


class Contact(Entry):
    """Contact itself"""
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

    def getPropByName(self, fld_name: str) -> str:
        d = {
            'fn': self.getFN,
            'family': self.getFamily,
            'given': self.getGiven,
            'email': self.getEmailList,
            'tel': self.getTelList
        }
        if fld := d.get(fld_name):
            return fld()
        return ''

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
