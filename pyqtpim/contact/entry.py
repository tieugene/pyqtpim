"""Contact itself

Most interesting (see contents:dict):
- fn:FN (card: 1): .fn.value
- n:N (card: ?): .n[...]:Name.value:dict.{family/given/additional}
- email:list(EMAIL) (card: ?)
- tel:list(TEL) (card: ?)
"""

import pprint
import vobject


class Contact:
    """Contact itself
    :todo: attributes
    """
    data: vobject.base.Component = None

    def __init__(self, src):
        self.data = src

    def getFN(self) -> str:
        return self.data.fn.value

    def getFamily(self):
        if n := self.data.contents.get('n'):
            return n[0].value.family
        else:
            return ''

    def getGiven(self):
        if n := self.data.contents.get('n'):
            return n[0].value.given
        else:
            return ''

    def getEmail(self):
        """:todo: preferable or list"""
        if email := self.data.contents.get('email'):
            return ", ".join([v.value for v in email])
        else:
            return ''

    def getTel(self):
        """:todo: preferable or list"""
        if tel := self.data.contents.get('tel'):
            return ", ".join([v.value for v in tel])
        else:
            return ''

    def print(self):
        def __fn():
            print(f"FN: {self.data.fn.value}")
        def __name():
            if n := self.data.contents.get('n'):
                print("N:", )
                v = n[0].value
                print(v.__dict__)
                # print(v.family)
        def __email():
            if email := self.data.contents.get('email'):
                print("Email:", )
                v = email[0]
                print(v.__dict__)
                print(f"value: {v.value}")
                if pref := v.params.get('PREF'):
                    print(f"pref: {bool(pref[0])}")
                print(", ".join([v.value for v in email]))
        print("==== VCARD ====")
        self.data.prettyPrint()
        print('----')
        pprint.pprint(self.data.__dict__)
        print('....')
