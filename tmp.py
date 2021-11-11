import os
from contact.collection import ContactList
from contact.mgr import ContactListManager

indir = '/Volumes/Trash/Documents/AB'

clm = ContactListManager()
clm.add(ContactList('AB', indir))
clm.reload()
clm.print()
