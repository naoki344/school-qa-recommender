from logging import Logger
from typing import List

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.sequences import SequensesDatasource
from app.model.classroom.classmate import Classmate
from app.model.classroom.classmate import ClassmateList
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.invite import ClassmateInvite
from app.model.classroom.invite import InviteKey
from app.model.user.user import UserId


class ClassroomDatasource:
    def __init__(self, client: DynamoDBClient,
                 sequenses_table: SequensesDatasource, logger: Logger) -> None:
        self.client = client
        self.sequenses_table = sequenses_table
        self.logger = logger

    def insert_item(self, item: Classroom) -> None:
        self.client.insert_item(item.to_dict(), "classroom_id")

    def put_item(self, item: Classroom) -> None:
        self.client.put_item(item.to_dict())

    def fetch_sequense_id(self) -> int:
        name = f"Dynamodb#{self.client.table.table_name}"
        _id = self.sequenses_table.fetch_sequense_id(name)
        return _id

    def find_by_id(self, classroom_id: ClassroomId) -> Classroom:
        data = self.client.get_item({'classroom_id': classroom_id.value})
        if data:
            return Classroom.from_dict(data)
        raise Exception('Classroom not found.')


class ClassmateDatasource:
    def __init__(self, client: DynamoDBClient, logger: Logger) -> None:
        self.client = client
        self.logger = logger

    def insert_item(self, classroom_id: ClassroomId,
                    classmate: Classmate) -> None:
        self.client.insert_item(
            {
                **classmate.to_dict(), "classroom_id": classroom_id.value
            }, "classroom_id", "user_id")

    def put_item(self, classroom_id: ClassroomId,
                 classmate: Classmate) -> None:
        self.client.put_item({
            **classmate.to_dict(), "classroom_id":
            classroom_id.value
        })

    def find(self, classroom_id: ClassroomId,
             classmate_id: UserId) -> Classmate:
        item = self.client.get_item({
            'classroom_id': classroom_id.value,
            'user_id': classmate_id.value
        })
        return Classmate.from_dict(item)

    def get_classmate_list(self, classroom_id: ClassroomId) -> Classmate:
        item_list = self.client.get_items(name='classroom_id',
                                          value=classroom_id.value)
        return ClassmateList.from_list(item_list)

    def find_by_user_id(self, user_id: UserId) -> List[list]:
        item_list = self.client.get_items(name='user_id',
                                          value=user_id.value,
                                          index_name='UserId-Index')
        return [[ClassroomId(item['classroom_id']),
                 Classmate.from_dict(item)] for item in item_list]


class ClassmateInviteDatasource:
    def __init__(self, client: DynamoDBClient, logger: Logger) -> None:
        self.client = client
        self.logger = logger

    def put_item(self, item: ClassmateInvite) -> None:
        self.client.put_item(item.to_dict())

    def find_by_invite_key(self, invite_key: InviteKey) -> ClassmateInvite:
        items = self.client.get_items(name='invite_key',
                                      value=invite_key.value,
                                      index_name='InviteKey-Index')
        return ClassmateInvite.from_dict(list(items)[0])
