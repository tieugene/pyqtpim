import os

from contact.data import Contact
from contact.collection import ContactList, ContactListManager

indir = '/Volumes/Trash/Documents/AB'
infile1 = os.path.join(indir, 'TI_Eugene.vcf')
infile2 = os.path.join(indir, 'Selta.vcf')


def test_clm():
    clm = ContactListManager()
    clm.itemAdd('AB', indir)
    # clm.reload()
    clm._print()


def test_cl():
    cl = ContactList(indir)
    cl.__load()
    cl._print()


def test_c():
    for infile in (infile1, infile2):
        Contact(infile)._print()


test_c()
# test_cl()
# test_clm()
