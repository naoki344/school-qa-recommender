from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.user import UserQueryService
from app.application.usecase.classroom import ApproveJoinClassroomRequest
from app.application.usecase.classroom import CreateClassroom
from app.application.usecase.classroom import FindClassroom
from app.application.usecase.classroom import RequestJoinClassroom
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.classroom.student import Student
from app.model.classroom.student import StudentList
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
        datasource = MagicMock()
        datasource.fetch_sequesnse_id = MagicMock(return_value=1)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        usecase = CreateClassroom(datasource=datasource,
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
        datasource.fetch_sequesnse_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            Classroom.from_dict(expect))
        datasource.put_item.assert_not_called()
        user_service.find.assert_called_once_with(user_id)
        self.assertEqual(result.to_dict(), expect)


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
            return_value=Classroom.from_dict(self.classroom_dict))
        student_datasource = MagicMock()
        student_datasource.get_student_list = MagicMock(
            return_value=StudentList.from_list([self.student_dict]))
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)
        usecase = FindClassroom(datasource=datasource,
                                student_datasource=student_datasource,
                                user_service=user_service,
                                logger=MagicMock())
        classroom, student_list = usecase.run(
            UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39-1'), ClassroomId(1))

        datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.user_service.find.assert_called_once_with(
            UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39-1'))
        self.assertEqual(classroom.to_dict(), self.classroom_dict)
        self.assertEqual(student_list.to_list(), [self.student_dict])

    def test_run_is_not_owner(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Classroom.from_dict(self.classroom_dict))
        student_datasource = MagicMock()
        student_datasource.get_student_list = MagicMock(
            return_value=StudentList.from_list([self.student_dict]))
        usecase = FindClassroom(datasource=datasource,
                                student_datasource=student_datasource,
                                user_service=MagicMock(spec=UserQueryService),
                                logger=MagicMock())
        classroom, student_list = usecase.run(UserId(1), ClassroomId(1))

        datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.user_service.find.assert_called_once_with(UserId(1))
        self.assertEqual(classroom.to_dict(), self.classroom_dict)
        self.assertEqual(student_list.to_list(), [])


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
                                       student_datasource=MagicMock(),
                                       user_service=user_service,
                                       logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id, ClassroomId(1))
        student_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }

        usecase.datasource.find_by_id.assert_called_once_with(ClassroomId(1))
        usecase.user_service.find.assert_called_once_with(user_id)
        usecase.student_datasource.insert_item.assert_called_once()
        self.assertEqual(result.to_dict(), student_dict)


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
        self.student_dict = {
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
        student_datasource = MagicMock()
        student_datasource.find = MagicMock(
            return_value=Student.from_dict(self.student_dict))
        usecase = ApproveJoinClassroomRequest(
            datasource=datasource,
            student_datasource=student_datasource,
            user_service=user_service,
            logger=MagicMock())
        user_id = UserId('owner')
        accept_user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        accept_user_list = [accept_user_id]
        classroom_id = ClassroomId(1)
        usecase.run(user_id, classroom_id, accept_user_list)

        usecase.datasource.find_by_id.assert_called_once_with(classroom_id)
        usecase.user_service.find.assert_called_once_with(user_id)
        usecase.student_datasource.find.assert_called_once_with(
            classroom_id, accept_user_id)
        usecase.student_datasource.put_item.assert_called_once_with(
            classroom_id,
            Student.from_dict({
                **self.student_dict, 'join_status': 'approved'
            }))
