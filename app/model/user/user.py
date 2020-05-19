from dataclasses import dataclass
from datetime import datetime

from app.utils.datetime import parse_datetime_as_jst


@dataclass(frozen=True)
class UserId:
    value: str


@dataclass(frozen=True)
class Email:
    value: str


@dataclass(frozen=True)
class Nickname:
    value: str


@dataclass(frozen=True)
class LastName:
    value: str


@dataclass(frozen=True)
class FirstName:
    value: str


@dataclass(frozen=True)
class LastNameKana:
    value: str


@dataclass(frozen=True)
class FirstNameKana:
    value: str


@dataclass(frozen=True)
class UserName:
    first_name: FirstName
    last_name: LastName

    @staticmethod
    def from_dict(data: dict) -> 'UserName':
        return UserName(first_name=FirstName(data['first_name']),
                        last_name=LastName(data['last_name']))

    def to_dict(self) -> dict:
        return {
            'first_name': self.first_name.value,
            'last_name': self.last_name.value
        }


@dataclass(frozen=True)
class CognitoUserSub:
    value: str


@dataclass(frozen=True)
class RegisterDate:
    value: datetime

    def to_string(self) -> str:
        return self.value.isoformat()

    @staticmethod
    def from_string(data: str) -> 'RegisterDate':
        return RegisterDate(parse_datetime_as_jst(data))


@dataclass(frozen=True)
class UserAvatarUrl:
    value: str


@dataclass(frozen=True)
class User:
    user_id: UserId
    nickname: Nickname
    user_name: UserName
    email: Email
    register_date: RegisterDate
    cognito_user_sub: CognitoUserSub

    @staticmethod
    def from_dict(data: dict):
        return User(user_id=UserId(data['user_id']),
                    nickname=Nickname(data['nickname']),
                    user_name=UserName.from_dict(data['user_name']),
                    email=Email(data['email']),
                    register_date=RegisterDate.from_string(
                        data['register_date']),
                    cognito_user_sub=CognitoUserSub(data['cognito_user_sub']))

    def to_dict(self):
        return {
            'user_id': self.user_id.value,
            'nickname': self.nickname.value,
            'user_name': self.user_name.to_dict(),
            'email': self.email.value,
            'register_date': self.register_date.to_string(),
            'cognito_user_sub': self.cognito_user_sub.value
        }
