from typing import Optional
from datetime import datetime as DateTime
from dataclasses import dataclass

from app.model.subject import SubjectType


@dataclass(frozen=True)
class QuestionId:
    value: int


@dataclass(frozen=True)
class Title:
    value: str


@dataclass(frozen=True)
class Caption:
    value: str


@dataclass(frozen=True)
class Contents:
    value: str


@dataclass(frozen=True)
class RegisterDate:
    value: DateTime

    # TODO: 後で実装
    @staticmethod
    def from_string(data: str) -> 'RegisterDate':
        return RegisterDate(data)

    # TODO: 後で実装
    def to_string(self):
        return self.value


@dataclass(frozen=True)
class RegisterUserId:
    value: str


@dataclass(frozen=True)
class Question:
    question_id: QuestionId
    register_user_id: RegisterUserId
    title: Title
    contents: Contents
    register_date: RegisterDate
    subject_type: SubjectType
    caption: Optional[Caption] = None

    @staticmethod
    def from_dict(data) -> 'Question':
        print(data)
        return Question(
            question_id=QuestionId(int(data['question_id'])),
            register_user_id=RegisterUserId(int(data['register_user_id'])),
            title=Title(str(data['title'])),
            contents=Contents(str(data['contents'])),
            register_date=RegisterDate.from_string(data['register_date']),
            subject_type=SubjectType[data['subject_type']],
            caption=Caption(str(data['caption']))
            if data.get('caption') else None)

    def to_dict(self):
        return {
            'question_id': self.question_id.value,
            'register_user_id': self.register_user_id.value,
            'title': self.title.value,
            'contents': self.contents.value,
            'register_date': self.register_date.to_string(),
            'subject_type': self.subject_type.name,
            'caption': self.caption.value if self.caption else None,
        }
