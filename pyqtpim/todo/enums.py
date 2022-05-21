"""Misc VTODO utility base and mappings.
:todo: add vobjects field names"""
from enum import IntEnum, unique, auto, Enum
from PySide2 import QtGui

# local constants

ColorRed = QtGui.QColorConstants.Red  # QtGui.QColorConstants.Svg.red
ColorOrange = QtGui.QColorConstants.Svg.orange
ColorYellow = QtGui.QColorConstants.Yellow
ColorGreen = QtGui.QColorConstants.Svg.lime
# ColorGreen = QtGui.QColorConstants.Green
ColorBlue = QtGui.QColorConstants.Blue
ColorLightBlue = QtGui.QColorConstants.Svg.dodgerblue
ColorLightGrey = QtGui.QColorConstants.LightGray
ColorGrey = QtGui.QColorConstants.Gray
ColorDarkGrey = QtGui.QColorConstants.DarkGray


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
    ("Store", None),
    ("Created", None),
    ("DTStamp", None),
    ("Modified", None),
    ("DTStart", None),
    ("Due", None),
    ("Completed", None),
    ('%', "Percent complete"),
    ('!', "Priority"),
    ("S", "Status"),
    ("Summary", None),
    ("Location", None),
)


# --- Class


# --- Status


TDecor_Status = '?…✓✗'
TColor_Status = (
    ColorBlue,
    ColorYellow,
    ColorGreen,
    ColorRed
)


# --- Priority


TDecor_Prio = '!!!!~↓↓↓↓'  # -1
TColor_Prio = (
    ColorRed,
    ColorOrange,
    ColorOrange,
    ColorOrange,
    ColorGreen,
    ColorLightBlue,
    ColorLightBlue,
    ColorLightBlue,
    ColorBlue,
)

TColor_Due = (
    ColorRed,
    ColorOrange,
    None,
    ColorLightGrey,
    ColorDarkGrey
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
