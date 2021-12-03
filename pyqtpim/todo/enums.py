from enum import IntEnum, unique, auto


@unique
class EClass(IntEnum):
    """CLASS property values"""
    Public = auto()
    Private = auto()
    Confidential = auto()


@unique
class EStatus(IntEnum):
    """STATUS property values"""
    NeedsAction = auto()
    InProcess = auto()
    Completed = auto()
    Cancelled = auto()


@unique
class ETrans(IntEnum):
    """TRANSPARENT property values"""
    Opaque = auto()
    Transparent = auto()


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
    Created = auto()        # ?
    Description = auto()    # ?
    DTStamp = auto()        # 1
    DTStart = auto()        # ?
    Due = auto()            # ?
    # Duration              # ?
    # ExDate                # *
    # Geo                   # ?
    LastModified = auto()   # ?
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
    Sequence = auto()       # ?
    Status = auto()         # ?
    Summary = auto()        # ?
    UID = auto()            # 1
    URL = auto()            # ?
