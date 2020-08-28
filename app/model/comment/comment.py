from dataclasses import dataclass
from dataclasses import replace
from enum import Enum
from enum import auto
from itertools import groupby
from operator import itemgetter
from typing import Dict
from typing import List
from typing import Optional

from app.model.register import RegisterDate
from app.model.register import RegisterUserId
from app.model.register import RegisterUserName
from app.model.user.user import User
from app.model.work.work import WorkId


@dataclass(frozen=True)
class CommentId:
    value: int


@dataclass(frozen=True)
class ParentCommentId:
    value: int


@dataclass(frozen=True)
class CommentType(Enum):
    topic = auto()
    message = auto()


@dataclass(frozen=True)
class CommentBody:
    value: str


@dataclass(frozen=True)
class WorkComment:
    comment_id: CommentId
    comment_type: CommentType
    parent_comment_id: Optional[ParentCommentId]
    work_id: WorkId
    body: CommentBody
    register_date: RegisterDate
    register_user_id: RegisterUserId
    register_user_name: RegisterUserName

    @staticmethod
    def from_dict(data: dict):
        return WorkComment(
            comment_id=CommentId(int(data['comment_id'])),
            comment_type=CommentType[str(data['comment_type'])],
            parent_comment_id=ParentCommentId(int(data['parent_comment_id']))
            if data.get('parent_comment_id') else None,
            work_id=WorkId(int(data['work_id'])),
            body=CommentBody(str(data['body'])),
            register_date=RegisterDate.from_string(data['register_date']),
            register_user_id=RegisterUserId(str(data['register_user_id'])),
            register_user_name=RegisterUserName(str(
                data['register_user_name'])))

    def to_dict(self):
        return {
            'comment_id':
            self.comment_id.value,
            'comment_type':
            self.comment_type.name,
            'parent_comment_id':
            self.parent_comment_id.value if self.parent_comment_id else None,
            'work_id':
            self.work_id.value,
            'body':
            self.body.value,
            'register_date':
            self.register_date.to_string(),
            'register_user_id':
            self.register_user_id.value,
            'register_user_name':
            self.register_user_name.value
        }

    def update(self, input_data: dict) -> 'WorkComment':
        if input_data.get('body'):
            return replace(self, **{'body': CommentBody(input_data['body'])})
        return self

    def is_own_comment(self, user: User):
        return self.register_user_id.value == user.user_id.value

    @staticmethod
    def create(work_id: WorkId, user: User, _id: int, comment_type: str,
               parent_comment_id: Optional[int], body: str):
        new_comment_type = CommentType[comment_type]
        if new_comment_type is CommentType.topic:
            if parent_comment_id:
                raise Exception(
                    'parent_comment_id must be None when comment_type qeual topic.'
                )
        return WorkComment(comment_id=CommentId(int(_id)),
                           comment_type=new_comment_type,
                           parent_comment_id=ParentCommentId(parent_comment_id)
                           if parent_comment_id else None,
                           body=CommentBody(body),
                           work_id=work_id,
                           register_date=RegisterDate.create(),
                           register_user_id=RegisterUserId(user.user_id.value),
                           register_user_name=RegisterUserName(
                               user.nickname.value))

    @staticmethod
    def create_main_topic(work_id: WorkId, user: User, _id: int):
        return WorkComment(comment_id=CommentId(int(_id)),
                           comment_type=CommentType.topic,
                           parent_comment_id=None,
                           body=CommentBody('メイン'),
                           work_id=work_id,
                           register_date=RegisterDate.create(),
                           register_user_id=RegisterUserId(user.user_id.value),
                           register_user_name=RegisterUserName(
                               user.nickname.value))


@dataclass(frozen=True)
class WorkCommentList:
    root_message_list: List[dict]
    topic_list: List[dict]
    topic_message_dict: Dict[int, List[dict]]

    @staticmethod
    def from_list(data: List[dict]) -> 'WorkCommentList':
        topic_list = []
        root_message_list = []
        topic_message_list = []
        sorted_data = sorted(data, key=itemgetter('comment_id'))
        for item in sorted_data:
            if item.get('parent_comment_id'):
                topic_message_list.append(item)
                continue

            if item['comment_type'] == 'topic':
                topic_list.append(item)
            else:
                root_message_list.append(item)

        sorted_data = sorted(topic_message_list,
                             key=itemgetter('parent_comment_id'))
        topic_message_dict = {}
        for k, v in groupby(sorted_data, key=itemgetter('parent_comment_id')):
            topic_message_dict[str(k)] = [item for item in v]

        return WorkCommentList(root_message_list=root_message_list,
                               topic_list=topic_list,
                               topic_message_dict=topic_message_dict)

    def to_response(self):
        return {
            "root_message_list": self.root_message_list,
            "topic_list": self.topic_list,
            "topic_message_dict": self.topic_message_dict
        }
