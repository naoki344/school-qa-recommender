import uuid
from dataclasses import dataclass
from typing import Dict

from app.model.classroom.classroom import ClassroomId
from app.model.datetime import DateTime
from app.utils.datetime import datetime_jst_now_delta


@dataclass(frozen=True)
class InviteKey:
    value: str

    @staticmethod
    def create():
        return InviteKey(str(uuid.uuid4()))


@dataclass(frozen=True)
class InviteLinkExpireDate(DateTime):
    value: str

    def create() -> 'InviteLinkExpireDate':
        return InviteLinkExpireDate(datetime_jst_now_delta(weeks=2))


@dataclass(frozen=True)
class ClassmateInvite:
    classroom_id: ClassroomId
    invite_key: InviteKey
    expire_date: InviteLinkExpireDate

    @staticmethod
    def create(classroom_id: ClassroomId) -> 'ClassmateInvite':
        return ClassmateInvite(classroom_id=classroom_id,
                               invite_key=InviteKey.create(),
                               expire_date=InviteLinkExpireDate.create())

    def to_dict(self) -> Dict[str, str]:
        return {
            'classroom_id': self.classroom_id.value,
            'invite_key': self.invite_key.value,
            'expire_date': self.expire_date.to_string(),
        }

    @staticmethod
    def from_dict(data) -> 'ClassmateInvite':
        return ClassmateInvite(
            classroom_id=ClassroomId(int(data['classroom_id'])),
            invite_key=InviteKey(str(data['invite_key'])),
            expire_date=InviteLinkExpireDate.from_string(data['expire_date']))
