from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.user import UserQueryService
from app.application.usecase.class_room import ApproveJoinClassRoomRequest
from app.application.usecase.class_room import CreateClassRoom
from app.application.usecase.class_room import FindClassRoom
from app.application.usecase.class_room import RequestJoinClassRoom
from app.model.class_room.class_room import ClassRoom
from app.model.class_room.class_room import ClassRoomId
from app.model.class_room.student import Student
from app.model.class_room.student import StudentList
from app.model.user.user import User
from app.model.user.user import UserId


class CreateClassRoomTest(TestCase):
    def setUp(self):
        self.class_room_dict = {
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
        datasource = MagicMock()
        datasource.fetch_sequesnse_id = MagicMock(return_value=1)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        usecase = CreateClassRoom(datasource=datasource,
                                  user_service=user_service,
                                  logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             item=deepcopy(self.class_room_dict))

        expect = {
            **self.class_room_dict, 'class_room_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
                'email': 'trombone344@gmail.com'
            }]
        }
        datasource.fetch_sequesnse_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            ClassRoom.from_dict(expect))
        datasource.put_item.assert_not_called()
        user_service.find.assert_called_once_with(user_id)
        self.assertEqual(result.to_dict(), expect)


class FindClassRoomTest(TestCase):
    def setUp(self):
        self.class_room_dict = {
            'class_room_id':
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
        self.student_dict = {
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
            return_value=ClassRoom.from_dict(self.class_room_dict))
        student_datasource = MagicMock()
        student_datasource.get_student_list = MagicMock(
            return_value=StudentList.from_list([self.student_dict]))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        usecase = FindClassRoom(datasource=datasource,
                                student_datasource=student_datasource,
                                user_service=user_service,
                                logger=MagicMock())
        class_room, student_list = usecase.run(
            UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39-1'), ClassRoomId(1))

        datasource.find_by_id.assert_called_once_with(ClassRoomId(1))
        usecase.user_service.find.assert_called_once_with(
            UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39-1'))
        self.assertEqual(class_room.to_dict(), self.class_room_dict)
        self.assertEqual(student_list.to_list(), [self.student_dict])

    def test_run_is_not_owner(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=ClassRoom.from_dict(self.class_room_dict))
        student_datasource = MagicMock()
        student_datasource.get_student_list = MagicMock(
            return_value=StudentList.from_list([self.student_dict]))
        usecase = FindClassRoom(datasource=datasource,
                                student_datasource=student_datasource,
                                user_service=MagicMock(spec=UserQueryService),
                                logger=MagicMock())
        class_room, student_list = usecase.run(UserId(1), ClassRoomId(1))

        datasource.find_by_id.assert_called_once_with(ClassRoomId(1))
        usecase.user_service.find.assert_called_once_with(UserId(1))
        self.assertEqual(class_room.to_dict(), self.class_room_dict)
        self.assertEqual(student_list.to_list(), [])


class RequestJoinClassRoomTest(TestCase):
    def setUp(self):
        self.class_room_dict = {
            'class_room_id':
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
            return_value=ClassRoom.from_dict(self.class_room_dict))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        usecase = RequestJoinClassRoom(datasource=datasource,
                                       student_datasource=MagicMock(),
                                       user_service=user_service,
                                       logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id, ClassRoomId(1))
        student_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }

        usecase.datasource.find_by_id.assert_called_once_with(ClassRoomId(1))
        usecase.user_service.find.assert_called_once_with(user_id)
        usecase.student_datasource.insert_item.assert_called_once()
        self.assertEqual(result.to_dict(), student_dict)


class ApproveJoinClassRoomRequestTest(TestCase):
    def setUp(self):
        self.class_room_dict = {
            'class_room_id':
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
        self.student_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=ClassRoom.from_dict(self.class_room_dict))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        student_datasource = MagicMock()
        student_datasource.find = MagicMock(
            return_value=Student.from_dict(self.student_dict))
        usecase = ApproveJoinClassRoomRequest(
            datasource=datasource,
            student_datasource=student_datasource,
            user_service=user_service,
            logger=MagicMock())
        user_id = UserId('owner')
        accept_user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        accept_user_list = [accept_user_id]
        class_room_id = ClassRoomId(1)
        usecase.run(user_id, class_room_id, accept_user_list)

        usecase.datasource.find_by_id.assert_called_once_with(class_room_id)
        usecase.user_service.find.assert_called_once_with(user_id)
        usecase.student_datasource.find.assert_called_once_with(
            class_room_id, accept_user_id)
        usecase.student_datasource.put_item.assert_called_once_with(
            class_room_id,
            Student.from_dict({
                **self.student_dict, 'join_status': 'approved'
            }))
