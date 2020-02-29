from logging import Logger
from typing import List

from app.application.query.user import UserQueryService
from app.dataaccess.dynamodb.class_room import ClassRoomDatasource
from app.dataaccess.dynamodb.class_room import ClassRoomStudentDatasource
from app.model.class_room.class_room import ClassRoom
from app.model.class_room.class_room import ClassRoomId
from app.model.class_room.student import Student
from app.model.user.user import UserId


class CreateClassRoom:
    def __init__(self, datasource: ClassRoomDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.user_service = user_service

    def run(self, user_id: UserId, item: dict) -> ClassRoom:
        _id = self.datasource.fetch_sequesnse_id()
        user = self.user_service.find(user_id)
        class_room = ClassRoom.create(_id, user, item)
        # TODO: validation
        self.datasource.insert_item(class_room)
        return class_room


class FindClassRoom:
    def __init__(self, datasource: ClassRoomDatasource,
                 logger: Logger) -> ClassRoom:
        self.datasource = datasource

    def run(self, class_room_id: ClassRoomId) -> ClassRoom:
        return self.datasource.find_by_id(class_room_id)


class RequestJoinClassRoom:
    '''生徒がクラスへの参加リクエストを送る機能'''
    def __init__(self, datasource: ClassRoomDatasource,
                 student_datasource: ClassRoomStudentDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.student_datasource = student_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, class_room_id: ClassRoomId) -> ClassRoom:
        user = self.user_service.find(user_id)
        class_room = self.datasource.find_by_id(class_room_id)
        if not class_room.can_join_request():
            raise Exception('can not join request this class room')
        student = Student.create(user)
        # TODO: 既に登録済みのユーザーの場合エラー文言を分ける
        self.student_datasource.insert_item(class_room.class_room_id, student)
        return student


class ApproveJoinClassRoomRequest:
    '''先生が生徒達のクラスへの参加を承認する機能'''
    def __init__(self, datasource: ClassRoomDatasource,
                 student_datasource: ClassRoomStudentDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.student_datasource = student_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, class_room_id: ClassRoomId,
            accept_user_list: List[UserId]) -> None:
        owner = self.user_service.find(user_id)
        class_room = self.datasource.find_by_id(class_room_id)

        if not class_room.is_owner(owner.user_id):
            raise Exception('can not approve join request')

        for student_id in accept_user_list:
            student = self.student_datasource.find(class_room_id, student_id)
            student = student.approve()
            self.student_datasource.put_item(class_room_id, student)
