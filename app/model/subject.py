from enum import Enum
from enum import auto
from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectType(Enum):
    math = auto()
    english = auto()
    japanease = auto()
    chemistry = auto()
