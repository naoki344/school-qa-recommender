from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from app.model.register import RegisterDate
from app.model.register import RegisterUserId
from app.model.register import RegisterUserName
from app.model.user.user import User


@dataclass(frozen=True)
class QuestionId:
    value: int


@dataclass(frozen=True)
class QuestionType(Enum):
    describing = auto()
    selectable = auto()
    discussion = auto()


@dataclass(frozen=True)
class SubjectName:
    value: str


@dataclass(frozen=True)
class SentenceContents:
    value: str

    def get_top_image_url(self) -> Optional[str]:
        soup = BeautifulSoup(self.value, features='html.parser')
        img = soup.find('img')
        if img is not None:
            return img.get('s3-key')
        return None

    def get_text(self):
        soup = BeautifulSoup(self.value, features='html.parser')
        return soup.get_text(strip=True)

    @staticmethod
    def create(data: str):
        soup = BeautifulSoup(data, features='html.parser')
        for img in soup.find_all('img'):
            img["s3-key"] = SentenceContents.parse_src(img['src'])
            img["src"] = ""
        return SentenceContents(soup.prettify())

    @staticmethod
    def parse_src(src: str):
        url = urlparse(src)
        return url.path.replace('/public/upload/', '')


@dataclass(frozen=True)
class QuestionImageUrl:
    value: str


@dataclass(frozen=True)
class SentenceSummary:
    value: str


@dataclass(frozen=True)
class QuestionSentence:
    contents: SentenceContents
    summary: SentenceSummary

    @staticmethod
    def from_dict(data):
        return QuestionSentence(contents=SentenceContents(data['contents']),
                                summary=SentenceSummary(data['summary']))

    def to_dict(self) -> Dict[str, any]:
        return {'contents': self.contents.value, 'summary': self.summary.value}

    @staticmethod
    def create(data):
        contents = SentenceContents.create(data['contents'])
        return QuestionSentence(contents=contents,
                                summary=SentenceSummary(
                                    contents.get_text()[:50].strip()))

    def get_top_image_url(self) -> Optional[str]:
        return self.contents.get_top_image_url()


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
    question_sentence: QuestionSentence
    register_date: RegisterDate
    subject_name: SubjectName
    question_type: QuestionType
    sort_tag_list: SortTagList

    @staticmethod
    def from_dict(data: Dict[str, any]) -> 'Question':
        return Question(
            question_id=QuestionId(int(data['question_id'])),
            register_user_id=RegisterUserId(str(data['register_user_id'])),
            register_user_name=RegisterUserName(str(
                data['register_user_name'])),
            question_sentence=QuestionSentence.from_dict(
                data['question_sentence']),
            register_date=RegisterDate.from_string(data['register_date']),
            subject_name=SubjectName(data['subject_name']),
            question_type=QuestionType[data['question_type']],
            sort_tag_list=SortTagList.from_list(data['sort_tag_list']))

    def to_dict(self) -> Dict[str, any]:
        return {
            'question_id': self.question_id.value,
            'register_user_id': self.register_user_id.value,
            'register_user_name': self.register_user_name.value,
            'question_sentence': self.question_sentence.to_dict(),
            'register_date': self.register_date.to_string(),
            'subject_name': self.subject_name.value,
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
            question_sentence=QuestionSentence.create(
                data['question_sentence']),
            register_date=RegisterDate.create(),
            subject_name=SubjectName(data['subject_name']),
            question_type=QuestionType[data['question_type']],
            sort_tag_list=SortTagList.from_list(data['sort_tag_list']))


@dataclass(frozen=True)
class QuestionCard:
    question_id: QuestionId
    question_sentence: QuestionSentence
    register_user_id: RegisterUserId
    register_user_name: RegisterUserName
    register_date: RegisterDate
    subject_name: SubjectName
    question_type: QuestionType
    sort_tag_list: SortTagList

    @staticmethod
    def from_db(data: Dict[str, any]) -> 'QuestionCard':
        return QuestionCard(
            question_id=QuestionId(int(data['question_id'])),
            register_user_id=RegisterUserId(str(data['register_user_id'])),
            register_user_name=RegisterUserName(str(
                data['register_user_name'])),
            question_sentence=QuestionSentence.from_dict(
                data['question_sentence']),
            register_date=RegisterDate.from_string(data['register_date']),
            subject_name=SubjectName(data['subject_name']),
            question_type=QuestionType[data['question_type']],
            sort_tag_list=SortTagList.from_list(data['sort_tag_list']))

    def to_response(self) -> Dict[str, any]:
        return {
            'question_id': self.question_id.value,
            'question_sentence': self.question_sentence.to_dict(),
            'image_url': self.question_sentence.get_top_image_url(),
            'register_user_id': self.register_user_id.value,
            'register_user_name': self.register_user_name.value,
            'register_date': self.register_date.to_string(),
            'subject_name': self.subject_name.value,
            'question_type': self.question_type.name,
            'sort_tag_list': self.sort_tag_list.to_list()
        }
