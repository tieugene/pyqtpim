# --- Model
from enum import unique, IntEnum


@unique
class EColNo(IntEnum):
    ID = 0
    Active = 1
    Name = 2
    Connection = 3


ColHeader = (  # Header
    "ID",
    '✓',
    "Name",
    "Connection"
)
