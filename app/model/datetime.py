from dataclasses import dataclass
from datetime import datetime as DateTime

from app.utils.datetime import datetime_jst_now
from app.utils.datetime import parse_datetime_as_jst


@dataclass(frozen=True)
class DateTime:
    value: DateTime

    @staticmethod
    def from_string(data: str) -> 'DateTime':
        return DateTime(parse_datetime_as_jst(data))

    def to_string(self):
        return self.value.isoformat()

    @staticmethod
    def create() -> 'DateTime':
        return DateTime(datetime_jst_now())
