"""Misc VTODO utility enums and mappings.
:todo: add vobjects field names"""
from enum import IntEnum, unique, auto, Enum
from PySide2 import QtGui

# local constants
ColorRed = QtGui.QColorConstants.Red  # QtGui.QColorConstants.Svg.red
# ColorOrange = QtGui.QColorConstants.Svg.orange
ColorYellow = QtGui.QColorConstants.Yellow
ColorGreen = QtGui.QColorConstants.Svg.lime
# ColorGreen = QtGui.QColorConstants.Green
ColorBlue = QtGui.QColorConstants.Blue
ColorLightBlue = QtGui.QColorConstants.Svg.dodgerblue


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
class EDBFld(Enum):
    """Database table field names
    :todo:"""
    ID = 'id'


# --- Model
@unique
class EColNo(IntEnum):  # was 0..14
    Store = 0
    Created = 1
    DTStamp = 2
    Modified = 3
    DTStart = 4
    Due = 5
    Completed = 6
    Progress = 7
    Prio = 8
    Status = 9
    Summary = 10
    Location = 11


ColHeader = (  # Header
    "Store",
    "Created",
    "DTStamp",
    "Modified",
    "DTStart",
    "Due",
    "Completed",
    '%',
    '!',
    "Status",
    "Summary",
    "Location",
)


# --- Class
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


# --- Status
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
TDecor_Status = '?…✓✗'
TColor_Status = (
    ColorBlue,
    ColorYellow,
    ColorGreen,
    ColorRed
)


# --- Priority
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

TDecor_Prio = '!!!!~↓↓↓↓'  # -1
TColor_Prio = (
    ColorRed,
    ColorLightBlue,
    ColorGreen,
)


# --- Sorting
@unique
class ESortBy(IntEnum):
    """List sorting order"""
    AsIs = auto()
    Name = auto()
    PrioDueName = auto()


# --- Filtering
@unique
class EFiltBy(IntEnum):
    """List filter rules"""
    All = auto()
    Closed = auto()
    Opened = auto()
    Today = auto()
    Tomorrow = auto()
