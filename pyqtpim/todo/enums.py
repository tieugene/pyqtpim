"""Misc VTODO utility enums and mappings.
:todo: add vobjects field names"""
from enum import IntEnum, unique, auto


@unique
class EProp(IntEnum):
    """VTODO properties (usual).
     (21..25 from 32 available)"""
    Attach = auto()         # *
    # Attendee              # *
    Categories = auto()     # *
    Class = auto()          # ?
    Comment = auto()        # *
    Completed = auto()      # ?
    Contact = auto()        # *
    Created = auto()        # ? auto
    Description = auto()    # ?
    DTStamp = auto()        # 1 auto
    DTStart = auto()        # ?
    Due = auto()            # ?
    # Duration              # ?
    # ExDate                # *
    # Geo                   # ?
    LastModified = auto()   # ? auto
    Location = auto()       # ?
    # Organizer             # ?
    Percent = auto()        # ? ==  PERCENT-COMPLETE
    Priority = auto()       # ?
    # RDate                 # *
    # RECURRENCE-ID         # ?
    RelatedTo = auto()      # *
    # REQUEST-STATUS        # *
    # Resources             # *
    RRule = auto()          # ?
    Sequence = auto()       # ? auto
    Status = auto()         # ?
    Summary = auto()        # ?
    UID = auto()            # 1 auto
    URL = auto()            # ?


@unique
class EClass(IntEnum):
    """CLASS property values"""
    Public = auto()
    Private = auto()
    Confidential = auto()


Raw2Enum_Class: dict[str, EClass] = {
    'PUBLIC': EClass.Public,
    'PRIVATE': EClass.Private,
    'CONFIDENTIAL': EClass.Confidential
}


@unique
class EStatus(IntEnum):
    """STATUS property values"""
    NeedsAction = auto()
    InProcess = auto()
    Completed = auto()
    Cancelled = auto()


Raw2Enum_Status: dict[str, EStatus] = {
    'NEEDS-ACTION': EStatus.NeedsAction,
    'IN-PROCESS': EStatus.InProcess,
    'COMPLETED': EStatus.Completed,
    'CANCELLED': EStatus.Cancelled
}
