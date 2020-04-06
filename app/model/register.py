from dataclasses import dataclass
from datetime import datetime as DateTime

from app.utils.datetime import datetime_jst_now
from app.utils.datetime import parse_datetime_as_jst


@dataclass(frozen=True)
class RegisterDate:
    value: DateTime

    @staticmethod
    def from_string(data: str) -> 'RegisterDate':
        return RegisterDate(parse_datetime_as_jst(data))

    def to_string(self):
        return self.value.isoformat()

    @staticmethod
    def create() -> 'RegisterDate':
        return RegisterDate(datetime_jst_now())


@dataclass(frozen=True)
class RegisterUserId:
    value: str


@dataclass(frozen=True)
class RegisterUserName:
    value: str
