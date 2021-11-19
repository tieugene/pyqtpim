from enum import IntEnum, unique


@unique
class EClass(IntEnum):
    Public = 1,
    Private = 2,
    Confidential = 3


@unique
class EStatus(IntEnum):
    NeedsAction = 1,
    InProcess = 2,
    Completed = 3,
    Cancelled = 4


@unique
class ETrans(IntEnum):
    Opaque = 1,
    Transparent = 2
