"""Exceptions"""


class ContactError(RuntimeError):
    """Contact basic error"""
    ...


class ContactLoadError(ContactError):
    """COntact loading exceptions"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg
