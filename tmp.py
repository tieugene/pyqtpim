import os

import vobject

from contact.entry import Contact
from contact.collection import ContactList, ContactListManager

indir = '/Volumes/Trash/Documents/AB'
infile1 = os.path.join(indir, 'TI_Eugene.vcf')
infile2 = os.path.join(indir, 'Selta.vcf')


def test_clm():
    clm = ContactListManager()
    clm.add('AB', ContactList(indir))
    clm.reload()
    clm.print()


def test_cl():
    cl = ContactList(indir)
    cl.reload()
    cl.print()


def test_c():
    for infile in (infile1, infile2):
        with open(infile, 'rt') as stream:
            c = Contact(vobject.readOne(stream))
            c.print()


test_c()
