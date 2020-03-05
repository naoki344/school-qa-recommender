from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.sequences import SequensesDatasource
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.student import Student
from app.model.classroom.student import StudentList
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

    def fetch_sequesnse_id(self) -> int:
        name = f"Dynamodb#{self.client.table.table_name}"
        _id = self.sequenses_table.fetch_sequense_id(name)
        return _id

    def find_by_id(self, classroom_id: ClassroomId) -> Classroom:
        data = self.client.get_item({'classroom_id': classroom_id.value})
        if data:
            return Classroom.from_dict(data)
        raise Exception('Classroom not found.')


class ClassroomStudentDatasource:
    def __init__(self, client: DynamoDBClient, logger: Logger) -> None:
        self.client = client
        self.logger = logger

    def insert_item(self, classroom_id: ClassroomId,
                    student: Student) -> None:
        self.client.insert_item(
            {
                **student.to_dict(), "classroom_id": classroom_id.value
            }, "classroom_id", "user_id")

    def put_item(self, classroom_id: ClassroomId, student: Student) -> None:
        self.client.put_item({
            **student.to_dict(), "classroom_id":
            classroom_id.value
        })

    def find(self, classroom_id: ClassroomId, student_id: UserId) -> Student:
        item = self.client.get_item({
            'classroom_id': classroom_id.value,
            'user_id': student_id.value
        })
        return Student.from_dict(item)

    def get_student_list(self, classroom_id: ClassroomId) -> Student:
        item_list = self.client.get_items(name='classroom_id',
                                          value=classroom_id.value)
        return StudentList.from_list(item_list)
