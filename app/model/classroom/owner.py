from dataclasses import dataclass
from typing import List

from app.model.user.user import Email
from app.model.user.user import Nickname
from app.model.user.user import User
from app.model.user.user import UserId


@dataclass(frozen=True)
class ClassroomOwner:
    user_id: UserId
    nickname: Nickname
    email: Email

    @staticmethod
    def from_dict(data):
        return ClassroomOwner(user_id=UserId(data['user_id']),
                              nickname=Nickname(data['nickname']),
                              email=Email(data['email']))

    def to_dict(self):
        return {
            'user_id': self.user_id.value,
            'nickname': self.nickname.value,
            'email': self.email.value
        }

    def create(user: User) -> 'ClassroomOwner':
        return ClassroomOwner(user_id=user.user_id,
                              nickname=user.nickname,
                              email=user.email)


@dataclass(frozen=True)
class ClassroomOwnerList:
    values: List[ClassroomOwner]

    @staticmethod
    def from_list(data) -> 'ClassroomOwnerList':
        return ClassroomOwnerList([ClassroomOwner.from_dict(d) for d in data])

    def to_list(self) -> List[dict]:
        return [s.to_dict() for s in self.values]

    def create(user: User) -> 'ClassroomOwnerList':
        return ClassroomOwnerList([ClassroomOwner.create(user)])

    def is_owner(self, user_id: UserId) -> bool:
        res = next(filter(lambda owner: owner.user_id == user_id, self.values),
                   None)
        if res:
            return True
        return False
