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
    Attach = auto()
    Categories = auto()
    Class = auto()
    Comment = auto()
    Completed = auto()
    Contact = auto()
    Created = auto()
    Description = auto()
    DTStamp = auto()
    DTStart = auto()
    Due = auto()
    # Duration
    # ExDate
    LastModified = auto()
    Location = auto()
    Percent = auto()   # PERCENT-COMPLETE
    Priority = auto()
    # RDate
    # RECURRENCE-ID
    RelatedTo = auto()
    RRule = auto()
    Sequence = auto()
    Status = auto()
    Summary = auto()
    UID = auto()
    URL = auto()
