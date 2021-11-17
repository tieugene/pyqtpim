"""Contact itself

Most interesting (see contents:dict):
- fn:FN (card: 1): .fn.value
- n:N (card: ?): .n[...]:Name.value:dict.{family/given/additional}
- email:list(EMAIL) (card: ?)
- tel:list(TEL) (card: ?)
"""

import vobject
# 3. local
from . import exc


class Contact:
    """Contact itself
    :todo: @proprty
    """
    __path: str = None
    __data: vobject.base.Component = None

    def __init__(self, path: str):
        with open(path, 'rt') as stream:
            if vcard := vobject.readOne(stream):
                if vcard.name == 'VCARD':
                    self.__data = vcard
                    self.__path = path
                else:
                    raise exc.ContactLoadError(f"It is not VCARD: {vcard.name}")
            else:
                raise exc.ContactLoadError(f"Cannot load vobject: {path}")
        if not self.__data:
            raise exc.ContactLoadError(f"File open error: {path}")

    def print(self):
        def __fn():
            print(f"FN: {self.__data.fn.value}")

        def __name():
            if n := self.__data.contents.get('n'):
                print("N:", )
                v = n[0].value
                print(v.__dict__)
                # print(v.family)

        def __email():
            if email := self.__data.contents.get('email'):
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

    @property
    def FN(self) -> str:
        return self.__get_fn()

    def __get_fn(self) -> str:
        return self.__data.fn.value

    @property
    def Family(self) -> str:
        return self.__get_family()

    def __get_family(self) -> str:
        if n := self.__data.contents.get('n'):
            return n[0].value.family
        return ''

    @property
    def Given(self) -> str:
        return self.__get_given()

    def __get_given(self) -> str:
        if n := self.__data.contents.get('n'):
            return n[0].value.given
        return ''

    @property
    def EmailList(self) -> str:
        return self.__get_email_list()

    def __get_email_list(self) -> str:
        """:todo: preferable or list"""
        if email := self.__data.contents.get('email'):
            return ", ".join([v.value for v in email])
        return ''

    @property
    def TelList(self) -> str:
        return self.__get_tel_list()

    def __get_tel_list(self) -> str:
        """:todo: preferable or list"""
        if tel := self.__data.contents.get('tel'):
            return ", ".join([v.value for v in tel])
        return ''

    def getPropByName(self, fld_name: str) -> str:
        d = {
            'fn': self.__get_fn,
            'family': self.__get_family,
            'given': self.__get_given,
            'email': self.__get_email_list,
            'tel': self.__get_tel_list
        }
        if fld := d.get(fld_name):
            return fld()
        return ''
