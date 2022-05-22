from enum import unique, IntEnum, auto


@unique
class EProp(IntEnum):
    """VTODO properties (usual).
     (21..25 from 32 available)"""
    Attach = auto()  # *
    # Attendee              # *
    Categories = auto()  # *
    Class = auto()  # ?
    Comment = auto()  # *
    Completed = auto()  # ? datetime.utc
    Contact = auto()  # *
    Created = auto()  # ? auto
    Description = auto()  # ?
    DTStamp = auto()  # 1 auto, datetime.utc
    DTStart = auto()  # ?
    Due = auto()  # ?
    # Duration              # ?
    # ExDate                # *
    # Geo                   # ?
    LastModified = auto()  # ? auto, datetime.utc
    Location = auto()  # ?
    # Organizer             # ?
    Progress = auto()  # ? ==  PERCENT-COMPLETE
    Priority = auto()  # ?
    # RDate                 # *
    # RECURRENCE-ID         # ?
    RelatedTo = auto()  # *
    # REQUEST-STATUS        # *
    # Resources             # *
    RRule = auto()  # ?
    Sequence = auto()  # ? auto
    Status = auto()  # ?
    Summary = auto()  # ?
    UID = auto()  # 1 auto
    URL = auto()  # ?


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
Enum2Raw_Class: dict[EClass, str] = {
    EClass.Public: 'PUBLIC',
    EClass.Private: 'PRIVATE',
    EClass.Confidential: 'CONFIDENTIAL',
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
Enum2Raw_Status: dict[EStatus, str] = {
    EStatus.NeedsAction: 'NEEDS-ACTION',
    EStatus.InProcess: 'IN-PROCESS',
    EStatus.Completed: 'COMPLETED',
    EStatus.Cancelled: 'CANCELLED'
}


@unique
class EPrio(IntEnum):
    """STATUS property values"""
    Low = auto()
    Normal = auto()
    High = auto()


Raw2Enum_Prio: tuple = (
    None,
    EPrio.High.value,
    EPrio.High.value,
    EPrio.High.value,
    EPrio.High.value,
    EPrio.Normal.value,
    EPrio.Low.value,
    EPrio.Low.value,
    EPrio.Low.value,
    EPrio.Low.value
)
