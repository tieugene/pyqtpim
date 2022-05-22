from enum import IntEnum, unique, auto


@unique
class EProp(IntEnum):
    """VCARD properties (usual)."""
    FN = auto()
    Family = auto()
    Name = auto()
    MidName = auto()
    Email = auto()
    Phone = auto()
