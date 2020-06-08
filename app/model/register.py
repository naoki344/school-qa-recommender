from dataclasses import dataclass

from app.model.datetime import DateTime


@dataclass(frozen=True)
class RegisterDate(DateTime):
    value: DateTime


@dataclass(frozen=True)
class RegisterUserId:
    value: str


@dataclass(frozen=True)
class RegisterUserName:
    value: str
