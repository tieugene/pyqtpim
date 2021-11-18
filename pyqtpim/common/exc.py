"""Exceptions"""


class EntryError(RuntimeError):
    """Entry basic error"""
    ...


class EntryLoadError(EntryError):
    """COntact loading exceptions"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg
