from dataclasses import dataclass

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
