from dataclasses import dataclass
from typing import List

from app.model.user.user import Email
from app.model.user.user import Nickname
from app.model.user.user import User
from app.model.user.user import UserId


@dataclass(frozen=True)
class ClassRoomOwner:
    user_id: UserId
    nickname: Nickname
    email: Email

    @staticmethod
    def from_dict(data):
        return ClassRoomOwner(user_id=UserId(data['user_id']),
                              nickname=Nickname(data['nickname']),
                              email=Email(data['email']))

    def to_dict(self):
        return {
            'user_id': self.user_id.value,
            'nickname': self.nickname.value,
            'email': self.email.value
        }

    def create(user: User) -> 'ClassRoomOwner':
        return ClassRoomOwner(user_id=user.user_id,
                              nickname=user.nickname,
                              email=user.email)


@dataclass(frozen=True)
class ClassRoomOwnerList:
    values: List[ClassRoomOwner]

    @staticmethod
    def from_list(data) -> 'ClassRoomOwnerList':
        return ClassRoomOwnerList([ClassRoomOwner.from_dict(d) for d in data])

    def to_list(self) -> List[str]:
        return [s.to_dict() for s in self.values]

    def create(user: User) -> 'ClassRoomOwnerList':
        return ClassRoomOwnerList([ClassRoomOwner.create(user)])
