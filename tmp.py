import os

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
