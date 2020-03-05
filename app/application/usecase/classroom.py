from logging import Logger
from typing import List
from typing import Tuple

from app.application.query.user import UserQueryService
from app.dataaccess.dynamodb.classroom import ClassroomDatasource
from app.dataaccess.dynamodb.classroom import ClassroomStudentDatasource
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.student import Student
from app.model.classroom.student import StudentList
from app.model.user.user import UserId


class CreateClassroom:
    def __init__(self, datasource: ClassroomDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.user_service = user_service

    def run(self, user_id: UserId, item: dict) -> Classroom:
        _id = self.datasource.fetch_sequesnse_id()
        user = self.user_service.find(user_id)
        classroom = Classroom.create(_id, user, item)
        # TODO: validation
        self.datasource.insert_item(classroom)
        return classroom


class FindClassroom:
    def __init__(self, datasource: ClassroomDatasource,
                 student_datasource: ClassroomStudentDatasource,
                 user_service: UserQueryService, logger: Logger) -> Classroom:
        self.datasource = datasource
        self.student_datasource = student_datasource
        self.user_service = user_service

    def run(self, user_id: UserId,
            classroom_id: ClassroomId) -> Tuple[Classroom, StudentList]:
        owner = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)
        student_list = self.student_datasource.get_student_list(classroom_id)
        if not classroom.is_owner(owner.user_id):
            student_list = student_list.approved_only()
        return classroom, student_list


class RequestJoinClassroom:
    '''生徒がクラスへの参加リクエストを送る機能'''
    def __init__(self, datasource: ClassroomDatasource,
                 student_datasource: ClassroomStudentDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.student_datasource = student_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, classroom_id: ClassroomId) -> Classroom:
        user = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)
        if not classroom.can_join_request():
            raise Exception('can not join request this class room')
        student = Student.create(user)
        # TODO: 既に登録済みのユーザーの場合エラー文言を分ける
        self.student_datasource.insert_item(classroom.classroom_id, student)
        return student


class ApproveJoinClassroomRequest:
    '''先生が生徒達のクラスへの参加を承認する機能'''
    def __init__(self, datasource: ClassroomDatasource,
                 student_datasource: ClassroomStudentDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.student_datasource = student_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, classroom_id: ClassroomId,
            accept_user_list: List[UserId]) -> None:
        owner = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)

        if not classroom.is_owner(owner.user_id):
            raise Exception('can not approve join request')

        for student_id in accept_user_list:
            student = self.student_datasource.find(classroom_id, student_id)
            student = student.approve()
            self.student_datasource.put_item(classroom_id, student)
