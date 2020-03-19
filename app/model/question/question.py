from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import Dict
from typing import List
from typing import Optional

from app.model.register import RegisterDate
from app.model.register import RegisterUserId
from app.model.register import RegisterUserName
from app.model.subject import SubjectType
from app.model.user.user import User


@dataclass(frozen=True)
class QuestionId:
    value: int


@dataclass(frozen=True)
class QuestionType(Enum):
    describing = auto()
    selectable = auto()


@dataclass(frozen=True)
class Text:
    value: str


@dataclass(frozen=True)
class ImageUrl:
    value: str


@dataclass(frozen=True)
class SentenceSummary:
    value: str


@dataclass(frozen=True)
class QuestionSentence:
    text: Text
    summary: SentenceSummary
    image_url: Optional[ImageUrl]

    @staticmethod
    def from_dict(data):
        return QuestionSentence(text=Text(data['text']),
                                summary=SentenceSummary(data['summary']),
                                image_url=ImageUrl(data['image_url'])
                                if data.get('image_url') else None)

    def to_dict(self) -> Dict[str, any]:
        return {
            'text': self.text.value,
            'summary': self.summary.value,
            'image_url': self.image_url.value if self.image_url else None
        }

    @staticmethod
    def create(data):
        return QuestionSentence(text=Text(data['text']),
                                summary=SentenceSummary(data['text'][:50]),
                                image_url=ImageUrl(data['image_url'])
                                if data.get('image_url') else None)


@dataclass(frozen=True)
class QuestionAnswer:
    text: Text
    image_url: Optional[ImageUrl]

    @staticmethod
    def from_dict(data):
        return QuestionAnswer(
            text=Text(data['text']),
            image_url=ImageUrl(
                data['image_url'] if data.get('image_url') else None))

    def to_dict(self) -> Dict[str, any]:
        return {
            'text': self.text.value,
            'image_url': self.image_url.value if self.image_url else None
        }


@dataclass(frozen=True)
class QuestionCommentary:
    text: Text
    image_url: Optional[ImageUrl]

    @staticmethod
    def from_dict(data):
        return QuestionCommentary(text=Text(data['text']),
                                  image_url=ImageUrl(data['image_url'])
                                  if data.get('image_url') else None)

    def to_dict(self) -> Dict[str, any]:
        return {
            'text': self.text.value,
            'image_url': self.image_url.value if self.image_url else None
        }


@dataclass(frozen=True)
class EstimatedTime:
    value: int


@dataclass(frozen=True)
class SortTag:
    value: str


@dataclass(frozen=True)
class SortTagList:
    values: List[SortTag]

    @staticmethod
    def from_list(data) -> 'SortTagList':
        return SortTagList([SortTag(d) for d in data])

    def to_list(self) -> List[str]:
        return [s.value for s in self.values]


@dataclass(frozen=True)
class Question:
    question_id: QuestionId
    register_user_id: RegisterUserId
    register_user_name: RegisterUserName
    estimated_time: EstimatedTime
    question_sentence: QuestionSentence
    question_answer: QuestionAnswer
    question_commentary: QuestionCommentary
    register_date: RegisterDate
    subject_type: SubjectType
    question_type: QuestionType
    sort_tag_list: SortTagList

    @staticmethod
    def from_dict(data: Dict[str, any]) -> 'Question':
        return Question(
            question_id=QuestionId(int(data['question_id'])),
            register_user_id=RegisterUserId(str(data['register_user_id'])),
            register_user_name=RegisterUserName(str(
                data['register_user_name'])),
            estimated_time=EstimatedTime(int(data['estimated_time'])),
            question_sentence=QuestionSentence.from_dict(
                data['question_sentence']),
            question_answer=QuestionAnswer.from_dict(data['question_answer']),
            question_commentary=QuestionCommentary.from_dict(
                data['question_commentary']),
            register_date=RegisterDate.from_string(data['register_date']),
            subject_type=SubjectType[data['subject_type']],
            question_type=QuestionType[data['question_type']],
            sort_tag_list=SortTagList.from_list(data['sort_tag_list']))

    def to_dict(self) -> Dict[str, any]:
        return {
            'question_id': self.question_id.value,
            'register_user_id': self.register_user_id.value,
            'register_user_name': self.register_user_name.value,
            'estimated_time': self.estimated_time.value,
            'question_sentence': self.question_sentence.to_dict(),
            'question_answer': self.question_answer.to_dict(),
            'question_commentary': self.question_commentary.to_dict(),
            'register_date': self.register_date.to_string(),
            'subject_type': self.subject_type.name,
            'question_type': self.question_type.name,
            'sort_tag_list': self.sort_tag_list.to_list()
        }

    @staticmethod
    def create(question_id: int, user: User, data: Dict[str,
                                                        any]) -> 'Question':
        return Question(
            question_id=QuestionId(int(question_id)),
            register_user_id=RegisterUserId(user.user_id.value),
            register_user_name=RegisterUserName(user.nickname.value),
            estimated_time=EstimatedTime(int(data['estimated_time'])),
            question_sentence=QuestionSentence.create(
                data['question_sentence']),
            question_answer=QuestionAnswer.from_dict(data['question_answer']),
            question_commentary=QuestionCommentary.from_dict(
                data['question_commentary']),
            register_date=RegisterDate.create(),
            subject_type=SubjectType[data['subject_type']],
            question_type=QuestionType[data['question_type']],
            sort_tag_list=SortTagList.from_list(data['sort_tag_list']))


@dataclass(frozen=True)
class QuestionCard:
    question_id: QuestionId
    question_sentence: QuestionSentence
    register_user_id: RegisterUserId
    register_user_name: RegisterUserName
    estimated_time: EstimatedTime
    register_date: RegisterDate
    subject_type: SubjectType
    question_type: QuestionType
    sort_tag_list: SortTagList

    @staticmethod
    def from_db(data: Dict[str, any]) -> 'QuestionCard':
        return QuestionCard(
            question_id=QuestionId(int(data['question_id'])),
            register_user_id=RegisterUserId(str(data['register_user_id'])),
            register_user_name=RegisterUserName(str(
                data['register_user_name'])),
            question_sentence=QuestionSentence.create(
                data['question_sentence']),
            estimated_time=EstimatedTime(int(data['estimated_time'])),
            register_date=RegisterDate.from_string(data['register_date']),
            subject_type=SubjectType[data['subject_type']],
            question_type=QuestionType[data['question_type']],
            sort_tag_list=SortTagList.from_list(data['sort_tag_list']))

    def to_dict(self) -> Dict[str, any]:
        return {
            'question_id': self.question_id.value,
            'question_sentence': self.question_sentence.to_dict(),
            'register_user_id': self.register_user_id.value,
            'register_user_name': self.register_user_name.value,
            'estimated_time': self.estimated_time.value,
            'register_date': self.register_date.to_string(),
            'subject_type': self.subject_type.name,
            'question_type': self.question_type.name,
            'sort_tag_list': self.sort_tag_list.to_list()
        }
