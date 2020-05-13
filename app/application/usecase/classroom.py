from logging import Logger
from typing import List
from typing import Tuple

from app.application.query.user import UserQueryService
from app.dataaccess.dynamodb.classroom import ClassmateDatasource
from app.dataaccess.dynamodb.classroom import ClassmateInviteDatasource
from app.dataaccess.dynamodb.classroom import ClassroomDatasource
from app.model.classroom.classmate import Classmate
from app.model.classroom.classmate import ClassmateList
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.invite import ClassmateInvite
from app.model.classroom.invite import InviteKey
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
        _id = self.datasource.fetch_sequense_id()
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
        user = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)
        classmate_list = self.classmate_datasource.get_classmate_list(
            classroom_id)
        if not classroom.is_owner(user.user_id):
            classmate_list = classmate_list.approved_only()
        return classroom, classmate_list


class CreateClassmateInviteLink:
    def __init__(self, datasource: ClassroomDatasource,
                 invite_datasource: ClassmateInviteDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.invite_datasource = invite_datasource
        self.user_service = user_service

    def run(self, user_id: UserId,
            classroom_id: ClassroomId) -> ClassmateInvite:
        user = self.user_service.find(user_id)
        classroom = self.datasource.find_by_id(classroom_id)
        if not classroom.is_owner(user.user_id):
            raise Exception('Can not create classroom invite link')
        classmate_invite = ClassmateInvite.create(classroom_id)
        self.invite_datasource.put_item(classmate_invite)
        return classmate_invite


class FindClassroomByInviteKey:
    def __init__(self, datasource: ClassroomDatasource,
                 invite_datasource: ClassmateInviteDatasource,
                 user_service: UserQueryService, logger: Logger) -> Classroom:
        self.datasource = datasource
        self.invite_datasource = invite_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, invite_key: InviteKey) -> Classroom:
        classmate_invite = self.invite_datasource.find_by_invite_key(
            invite_key=invite_key)
        classroom = self.datasource.find_by_id(classmate_invite.classroom_id)
        return classroom


class RequestJoinClassroomByInviteKey:
    def __init__(self, datasource: ClassroomDatasource,
                 classmate_datasource: ClassmateDatasource,
                 invite_datasource: ClassmateInviteDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.classmate_datasource = classmate_datasource
        self.invite_datasource = invite_datasource
        self.user_service = user_service

    def run(self, user_id: UserId, invite_key: InviteKey) -> Classmate:
        user = self.user_service.find(user_id)
        classmate_invite = self.invite_datasource.find_by_invite_key(
            invite_key=invite_key)
        classmate = Classmate.create(user)
        # TODO: 既に登録済みのユーザーの場合エラー文言を分ける
        self.classmate_datasource.insert_item(classmate_invite.classroom_id,
                                              classmate)
        return classmate


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
        my_classmate_list = self.classmate_datasource.find_by_user_id(
            user.user_id)
        items = []
        for classroom_id, my_classmate_info in my_classmate_list:
            classroom = self.datasource.find_by_id(classroom_id)
            classmate_list = self.classmate_datasource.get_classmate_list(
                classroom_id)
            if not classroom.is_owner(user_id):
                classmate_list = classmate_list.approved_only()
            items.append(
                MyClassroom(classroom=classroom,
                            classmate=my_classmate_info,
                            classmate_list=classmate_list))
        return MyClassroomList(items)
