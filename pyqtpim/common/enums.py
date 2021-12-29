# --- Model
from enum import unique, IntEnum, Enum


class SetGroup(Enum):
    Contacts = 'contacts'
    ToDo = 'todo'


@unique
class EColNo(IntEnum):
    Name = 0
    Connection = 1
    Active = 2


ColHeader = (  # Header
    "Name",
    "Connection",
    '✓'
)
