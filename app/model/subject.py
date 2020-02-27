from dataclasses import dataclass
from enum import Enum
from enum import auto


@dataclass(frozen=True)
class SubjectType(Enum):
    math = auto()
    english = auto()
    japanease = auto()
    chemistry = auto()
    world_history = auto()
    japanease_history = auto()
    geography = auto()
    contemporary_society = auto()
    biology = auto()
    physics = auto()
    earth_science = auto()
