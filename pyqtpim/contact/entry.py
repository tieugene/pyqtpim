"""Contact itself"""

import vobject


class Contact:
    data: vobject.base.Component = None

    def __init__(self, src):
        self.data = src

    def print(self):
        self.data.prettyPrint()
