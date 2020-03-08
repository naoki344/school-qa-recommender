from logging import Logger
from typing import List
from typing import Tuple

from app.application.query.user import UserQueryService
from app.dataaccess.dynamodb.classroom import ClassmateDatasource
from app.dataaccess.dynamodb.classroom import ClassroomDatasource
from app.model.classroom.classmate import Classmate
from app.model.classroom.classmate import ClassmateList
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.my_classroom import MyClassroom
from app.model.classroom.my_classroom import MyClassroomList
from app.model.user.user import UserId


class CreateClassroom:
    def __init__(self, datasource: ClassroomDatasource,
                 classmate_datasource: ClassmateDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.classmate_datasource = classmate_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, item: dict) -> Classroom:
        _id = self.datasource.fetch_sequesnse_id()
        user = self.user_service.find(user_id)
        classroom = Classroom.create(_id, user, item)
        # TODO: validation
        self.datasource.insert_item(classroom)
        classmate = Classmate.create_owner(user)
        self.classmate_datasource.insert_item(classroom.classroom_id,
                                              classmate)
        return classroom


class FindClassroom:
    def __init__(self, datasource: ClassroomDatasource,
                 classmate_datasource: ClassmateDatasource,
                 user_service: UserQueryService, logger: Logger) -> Classroom:
        self.datasource = datasource
        self.classmate_datasource = classmate_datasource
        self.user_service = user_service

    def run(self, user_id: UserId,
            classroom_id: ClassroomId) -> Tuple[Classroom, ClassmateList]:
        owner = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)
        classmate_list = self.classmate_datasource.get_classmate_list(
            classroom_id)
        if not classroom.is_owner(owner.user_id):
            classmate_list = classmate_list.approved_only()
        return classroom, classmate_list


class RequestJoinClassroom:
    '''生徒がクラスへの参加リクエストを送る機能'''
    def __init__(self, datasource: ClassroomDatasource,
                 classmate_datasource: ClassmateDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.classmate_datasource = classmate_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, classroom_id: ClassroomId) -> Classroom:
        user = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)
        if not classroom.can_join_request():
            raise Exception('can not join request this class room')
        classmate = Classmate.create(user)
        # TODO: 既に登録済みのユーザーの場合エラー文言を分ける
        self.classmate_datasource.insert_item(classroom.classroom_id,
                                              classmate)
        return classmate


class ApproveJoinClassroomRequest:
    '''先生が生徒達のクラスへの参加を承認する機能'''
    def __init__(self, datasource: ClassroomDatasource,
                 classmate_datasource: ClassmateDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.classmate_datasource = classmate_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, classroom_id: ClassroomId,
            accept_user_list: List[UserId]) -> None:
        owner = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)

        if not classroom.is_owner(owner.user_id):
            raise Exception('can not approve join request')

        for classmate_id in accept_user_list:
            classmate = self.classmate_datasource.find(classroom_id,
                                                       classmate_id)
            classmate = classmate.approve()
            self.classmate_datasource.put_item(classroom_id, classmate)


class GetMyClassroomList:
    def __init__(self, datasource: ClassroomDatasource,
                 classmate_datasource: ClassmateDatasource,
                 user_service: UserQueryService, logger: Logger) -> Classroom:
        self.datasource = datasource
        self.classmate_datasource = classmate_datasource
        self.user_service = user_service

    def run(self, user_id: UserId) -> MyClassroomList:
        user = self.user_service.find(user_id)
        classmate_list = self.classmate_datasource.find_by_user_id(
            user.user_id)
        items = []
        for classroom_id, classmate in classmate_list:
            classroom = self.datasource.find_by_id(classroom_id)
            items.append(MyClassroom(classroom=classroom, classmate=classmate))
        return MyClassroomList(items)