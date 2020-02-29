from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.sequences import SequensesDatasource
from app.model.class_room.class_room import ClassRoom
from app.model.class_room.class_room import ClassRoomId
from app.model.class_room.student import Student
from app.model.class_room.student import StudentList
from app.model.user.user import UserId


class ClassRoomDatasource:
    def __init__(self, client: DynamoDBClient,
                 sequenses_table: SequensesDatasource, logger: Logger) -> None:
        self.client = client
        self.sequenses_table = sequenses_table
        self.logger = logger

    def insert_item(self, item: ClassRoom) -> None:
        self.client.insert_item(item.to_dict(), "class_room_id")

    def put_item(self, item: ClassRoom) -> None:
        self.client.put_item(item.to_dict())

    def fetch_sequesnse_id(self) -> int:
        name = f"Dynamodb#{self.client.table.table_name}"
        _id = self.sequenses_table.fetch_sequense_id(name)
        return _id

    def find_by_id(self, class_room_id: ClassRoomId) -> ClassRoom:
        data = self.client.get_item({'class_room_id': class_room_id.value})
        if data:
            return ClassRoom.from_dict(data)
        raise Exception('ClassRoom not found.')


class ClassRoomStudentDatasource:
    def __init__(self, client: DynamoDBClient, logger: Logger) -> None:
        self.client = client
        self.logger = logger

    def insert_item(self, class_room_id: ClassRoomId,
                    student: Student) -> None:
        self.client.insert_item(
            {
                **student.to_dict(), "class_room_id": class_room_id.value
            }, "class_room_id", "user_id")

    def put_item(self, class_room_id: ClassRoomId, student: Student) -> None:
        self.client.put_item({
            **student.to_dict(), "class_room_id":
            class_room_id.value
        })

    def find(self, class_room_id: ClassRoomId, student_id: UserId) -> Student:
        item = self.client.get_item({
            'class_room_id': class_room_id.value,
            'user_id': student_id.value
        })
        return Student.from_dict(item)

    def get_student_list(self, class_room_id: ClassRoomId) -> Student:
        item_list = self.client.get_items(name='class_room_id',
                                          value=class_room_id.value)
        return StudentList.from_list(item_list)
