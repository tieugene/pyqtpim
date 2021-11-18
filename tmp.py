import os
import sys
import inspect

from contact import ContactList, ContactListManager

indir = '/Volumes/Trash/Documents/AB'
infile1 = os.path.join(indir, 'TI_Eugene.vcf')
infile2 = os.path.join(indir, 'Selta.vcf')


def test_clm():
    clm = ContactListManager()
    clm.itemAdd('AB', indir)
    # clm.reload()
    clm.print()


def test_cl():
    cl = ContactList(indir)
    cl.print()


# def test_c():
#    for infile in (infile1, infile2):
#        Contact(infile).print()


# test_c()
# test_cl()
# test_clm()

class MyClass(object):
    def myfunc(self):
        print(f"Virtual: {__class__.__name__}.{inspect.currentframe().f_code.co_name}()")


# dir(MyClass().myfunc)
MyClass().myfunc()
