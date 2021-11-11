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

    def print(self):
        print("==== VCARD ====")
        self.data.prettyPrint()
        print('----')
        pprint.pprint(self.data.__dict__)
        print('....')
        print(f"FN: {self.data.fn.value}")
        if n := self.data.contents.get('n'):
            print("N:", )
            n = n[0].value
            print(n.__dict__)
            print(n.family)
