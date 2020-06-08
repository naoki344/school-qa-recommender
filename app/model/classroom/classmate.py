from dataclasses import dataclass
from dataclasses import replace
from enum import Enum
from enum import auto
from typing import List

from app.model.user.user import Email
from app.model.user.user import Nickname
from app.model.user.user import User
from app.model.user.user import UserId


class JoinStatus(Enum):
    owner = auto()
    requested = auto()
    approved = auto()
    rejected = auto()

    def is_join(self):
        allow_status = [JoinStatus.owner, JoinStatus.approved]
        if self.join_status in allow_status:
            return True
        return False


@dataclass(frozen=True)
class Classmate:
    user_id: UserId
    nickname: Nickname
    email: Email
    join_status: JoinStatus

    @staticmethod
    def from_dict(data: dict) -> 'Classmate':
        return Classmate(user_id=UserId(data['user_id']),
                         nickname=Nickname(data['nickname']),
                         email=Email(data['email']),
                         join_status=JoinStatus[data['join_status']])

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id.value,
            'nickname': self.nickname.value,
            'email': self.email.value,
            'join_status': self.join_status.name
        }

    def create(user: User) -> 'Classmate':
        return Classmate(user_id=user.user_id,
                         nickname=user.nickname,
                         email=user.email,
                         join_status=JoinStatus.requested)

    def create_owner(user: User) -> 'Classmate':
        return Classmate(user_id=user.user_id,
                         nickname=user.nickname,
                         email=user.email,
                         join_status=JoinStatus.owner)

    def approve(self) -> 'Classmate':
        if self.join_status is JoinStatus.approved:
            raise Exception('This classmate already approved.')
        return replace(self, join_status=JoinStatus.approved)


@dataclass(frozen=True)
class ClassmateList:
    values: List[Classmate]

    @staticmethod
    def from_list(data) -> 'ClassmateList':
        return ClassmateList([Classmate.from_dict(d) for d in data])

    def to_list(self) -> List[dict]:
        return [s.to_dict() for s in self.values]

    def approved_only(self) -> 'ClassmateList':
        allow_status = [JoinStatus.approved, JoinStatus.owner]
        return ClassmateList(
            [item for item in self.values if item.join_status in allow_status])
