from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import Optional

from app.model.classroom.classroom import ClassroomId
from app.model.question.question import Question
from app.model.register import RegisterDate
from app.model.register import RegisterUserId
from app.model.register import RegisterUserName
from app.model.user.user import User


@dataclass(frozen=True)
class WorkId:
    value: int


@dataclass(frozen=True)
class WorkType(Enum):
    discussion = auto()


@dataclass(frozen=True)
class WorkTitle:
    value: str


@dataclass(frozen=True)
class WorkCaption:
    value: str


@dataclass(frozen=True)
class WorkImageUrl:
    value: str


@dataclass(frozen=True)
class OriginId:
    value: int


@dataclass(frozen=True)
class OriginType(Enum):
    question = auto()


@dataclass(frozen=True)
class Work:
    work_id: WorkId
    work_type: WorkType
    classroom_id: ClassroomId
    title: WorkTitle
    caption: WorkCaption
    image_url: Optional[WorkImageUrl]
    origin_id: OriginId
    origin_type: OriginType
    register_date: RegisterDate
    register_user_id: RegisterUserId
    register_user_name: RegisterUserName

    @staticmethod
    def from_dict(data: dict):
        return Work(
            work_id=WorkId(int(data['work_id'])),
            work_type=WorkType[data['work_type']],
            classroom_id=ClassroomId(data['classroom_id']),
            title=WorkTitle(str(data['title'])),
            caption=WorkCaption(str(data['caption'])),
            image_url=WorkImageUrl(str(data['image_url']))
            if data.get('image_url') else None,
            origin_id=OriginId(int(data['origin_id'])),
            origin_type=OriginType[data['origin_type']],
            register_date=RegisterDate.from_string(data['register_date']),
            register_user_id=RegisterUserId(str(data['register_user_id'])),
            register_user_name=RegisterUserName(str(
                data['register_user_name'])))

    def to_dict(self):
        return {
            'work_id': self.work_id.value,
            'work_type': self.work_type.name,
            'classroom_id': self.classroom_id.value,
            'title': self.title.value,
            'caption': self.caption.value,
            'image_url': self.image_url.value if self.image_url else None,
            'origin_id': self.origin_id.value,
            'origin_type': self.origin_type.name,
            'register_date': self.register_date.to_string(),
            'register_user_id': self.register_user_id.value,
            'register_user_name': self.register_user_name.value
        }

    @staticmethod
    def create_from_question(_id: int, classroom_id: ClassroomId, user: User,
                             question: Question, data: dict):
        return Work(work_id=WorkId(int(_id)),
                    work_type=WorkType.discussion,
                    classroom_id=classroom_id,
                    title=WorkTitle(str(data['title'])),
                    caption=WorkCaption(str(data['caption'])),
                    image_url=WorkImageUrl(
                        question.question_sentence.get_top_image_url()),
                    origin_id=OriginId(int(question.question_id.value)),
                    origin_type=OriginType.question,
                    register_date=RegisterDate.create(),
                    register_user_id=RegisterUserId(user.user_id.value),
                    register_user_name=RegisterUserName(user.nickname.value))
