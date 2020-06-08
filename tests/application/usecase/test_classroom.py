from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.user import UserQueryService
from app.application.usecase.classroom import ApproveJoinClassroomRequest
from app.application.usecase.classroom import CreateClassmateInviteLink
from app.application.usecase.classroom import CreateClassroom
from app.application.usecase.classroom import FindClassroom
from app.application.usecase.classroom import FindClassroomByInviteKey
from app.application.usecase.classroom import GetMyClassroomList
from app.application.usecase.classroom import RequestJoinClassroom
from app.application.usecase.classroom import RequestJoinClassroomByInviteKey
from app.dataaccess.dynamodb.classroom import ClassroomDatasource
from app.model.classroom.classmate import Classmate
from app.model.classroom.classmate import ClassmateList
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.invite import ClassmateInvite
from app.model.classroom.invite import InviteKey
from app.model.classroom.my_classroom import MyClassroomList
from app.model.user.user import User
from app.model.user.user import UserId


class CreateClassroomTest(TestCase):
    def setUp(self):
        self.classroom_dict = {
            'name': 'test name',
            'image_url': 'https://example.example.com/test.jpg',
            'publish_type': 'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity': 10,
            'caption': 'test caption'
        }
        self.user_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)

    def test_run(self):
        # datasource の作成
        datasource = MagicMock(spec=ClassroomDatasource)
        datasource.fetch_sequense_id = MagicMock(return_value=1)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        usecase = CreateClassroom(datasource=datasource,
                                  classmate_datasource=MagicMock(),
                                  user_service=user_service,
                                  logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             item=deepcopy(self.classroom_dict))

        expect = {
            **self.classroom_dict, 'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
                'email': 'trombone344@gmail.com'
            }]
        }
        datasource.fetch_sequense_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            Classroom.from_dict(expect))
        datasource.put_item.assert_not_called()
        user_service.find.assert_called_once_with(user_id)
        self.assertEqual(result.to_dict(), expect)

        usecase.classmate_datasource.insert_item.assert_called_once_with(
            ClassroomId(1), Classmate.create_owner(self.user))


class FindClassroomTest(TestCase):
    def setUp(self):
        self.classroom_dict = {
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39-1',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        }
        self.classmate_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.user_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)

    def test_run_is_owner(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Classroom.from_dict(self.classroom_dict))
        classmate_datasource = MagicMock()
        classmate_datasource.get_classmate_list = MagicMock(
            return_value=ClassmateList.from_list([self.classmate_dict]))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        usecase = FindClassroom(datasource=datasource,
                                classmate_datasource=classmate_datasource,
                                user_service=user_service,
                                logger=MagicMock())
        classroom, classmate_list = usecase.run(
            UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39-1'), ClassroomId(1))

        datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.user_service.find.assert_called_once_with(
            UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39-1'))
        self.assertEqual(classroom.to_dict(), self.classroom_dict)
        self.assertEqual(classmate_list.to_list(), [self.classmate_dict])

    def test_run_is_not_owner(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Classroom.from_dict(self.classroom_dict))
        classmate_datasource = MagicMock()
        classmate_datasource.get_classmate_list = MagicMock(
            return_value=ClassmateList.from_list([self.classmate_dict]))
        usecase = FindClassroom(datasource=datasource,
                                classmate_datasource=classmate_datasource,
                                user_service=MagicMock(spec=UserQueryService),
                                logger=MagicMock())
        classroom, classmate_list = usecase.run(UserId(1), ClassroomId(1))

        datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.user_service.find.assert_called_once_with(UserId(1))
        self.assertEqual(classroom.to_dict(), self.classroom_dict)
        self.assertEqual(classmate_list.to_list(), [])


class RequestJoinClassroomTest(TestCase):
    def setUp(self):
        self.classroom_dict = {
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39-1',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'public',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        }
        self.user_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Classroom.from_dict(self.classroom_dict))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        usecase = RequestJoinClassroom(datasource=datasource,
                                       classmate_datasource=MagicMock(),
                                       user_service=user_service,
                                       logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id, ClassroomId(1))
        classmate_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }

        usecase.datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.user_service.find.assert_called_once_with(user_id)
        usecase.classmate_datasource.insert_item.assert_called_once()
        self.assertEqual(result.to_dict(), classmate_dict)


class CreateClassmateInviteLinkTest(TestCase):
    def setUp(self):
        self.classroom_dict = {
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39-1',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'public',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        }
        self.user_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Classroom.from_dict(self.classroom_dict))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        usecase = CreateClassmateInviteLink(datasource=datasource,
                                            invite_datasource=MagicMock(),
                                            user_service=user_service,
                                            logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id, ClassroomId(1))
        usecase.datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.user_service.find.assert_called_once_with(user_id)
        usecase.invite_datasource.put_item.assert_called_once()
        self.assertEqual(result.classroom_id, ClassroomId(1))


class FindClassroomByInviteKeyTest(TestCase):
    def setUp(self):
        self.classroom = Classroom.from_dict({
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39-1',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'public',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        })
        self.invite = ClassmateInvite.from_dict({
            'classroom_id':
            1,
            'invite_key':
            '79434gatbgare',
            'expire_date':
            '2020-02-15T00:18:16.874000+09:00'
        })

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(return_value=self.classroom)
        user_service = MagicMock(spec=UserQueryService)
        invite_datasource = MagicMock()
        invite_datasource.find_by_invite_key = MagicMock(
            return_value=self.invite)
        usecase = FindClassroomByInviteKey(datasource=datasource,
                                           invite_datasource=invite_datasource,
                                           user_service=user_service,
                                           logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        invite_key = InviteKey('79434gatbgare')
        result = usecase.run(invite_key)
        usecase.invite_datasource.find_by_invite_key.assert_called_once_with(
            invite_key=invite_key)
        usecase.datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        self.assertEqual(result, self.classroom)


class RequestJoinClassroomByInviteKeyTest(TestCase):
    def setUp(self):
        self.user_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)
        self.invite = ClassmateInvite.from_dict({
            'classroom_id':
            1,
            'invite_key':
            '79434gatbgare',
            'expire_date':
            '2020-02-15T00:18:16.874000+09:00'
        })
        self.classmate = Classmate.from_dict({
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        })

    def test_run_ok(self):
        datasource = MagicMock()
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        invite_datasource = MagicMock()
        invite_datasource.find_by_invite_key = MagicMock(
            return_value=self.invite)
        usecase = RequestJoinClassroomByInviteKey(
            datasource=datasource,
            classmate_datasource=MagicMock(),
            invite_datasource=invite_datasource,
            user_service=user_service,
            logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        invite_key = InviteKey('79434gatbgare')
        result = usecase.run(user_id, invite_key)
        usecase.invite_datasource.find_by_invite_key.assert_called_once_with(
            invite_key=invite_key)
        usecase.classmate_datasource.insert_item.assert_called_once()
        self.assertEqual(result, self.classmate)


class ApproveJoinClassroomRequestTest(TestCase):
    def setUp(self):
        self.classroom_dict = {
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': 'owner',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': 'owner2',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'public',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        }
        self.user_dict = {
            'user_id': 'owner',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)
        self.classmate_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Classroom.from_dict(self.classroom_dict))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        classmate_datasource = MagicMock()
        classmate_datasource.find = MagicMock(
            return_value=Classmate.from_dict(self.classmate_dict))
        usecase = ApproveJoinClassroomRequest(
            datasource=datasource,
            classmate_datasource=classmate_datasource,
            user_service=user_service,
            logger=MagicMock())
        user_id = UserId('owner')
        accept_user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        accept_user_list = [accept_user_id]
        classroom_id = ClassroomId(1)
        usecase.run(user_id, classroom_id, accept_user_list)

        usecase.datasource.find_by_id.assert_called_once_with(classroom_id)
        usecase.user_service.find.assert_called_once_with(user_id)
        usecase.classmate_datasource.find.assert_called_once_with(
            classroom_id, accept_user_id)
        usecase.classmate_datasource.put_item.assert_called_once_with(
            classroom_id,
            Classmate.from_dict({
                **self.classmate_dict, 'join_status':
                'approved'
            }))


class GetMyClassroomListTest(TestCase):
    def setUp(self):
        self.classroom_dict = {
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39-1',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        }
        self.classmate_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.user_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)

        self.classmate_list = [{
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }, {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af392',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'approved'
        }]

    def test_run_is_owner(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Classroom.from_dict(self.classroom_dict))
        classmate_datasource = MagicMock()
        classmate_datasource.find_by_user_id = MagicMock(return_value=[[
            ClassroomId(1),
            Classmate.from_dict(self.classmate_dict)
        ]])
        classmate_datasource.get_classmate_list = MagicMock(
            return_value=ClassmateList.from_list(self.classmate_list))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        usecase = GetMyClassroomList(datasource=datasource,
                                     classmate_datasource=classmate_datasource,
                                     user_service=user_service,
                                     logger=MagicMock())
        result = usecase.run(UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39'))
        usecase.datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.classmate_datasource.find_by_user_id.assert_called_once_with(
            UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39'))
        usecase.classmate_datasource.get_classmate_list.assert_called_once_with(
            ClassroomId(1))
        self.assertEqual(
            result,
            MyClassroomList.from_list([{
                "classmate": self.classmate_dict,
                "classroom": self.classroom_dict,
                "classmate_list": self.classmate_list
            }]))
