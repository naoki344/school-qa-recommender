from unittest import TestCase

from app.model.class_room.student import Student
from app.model.class_room.student import StudentList
from app.model.user.user import User


class StudentTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dict(self):
        student_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.assertEqual(
            Student.from_dict(student_dict).to_dict(), student_dict)

    def test_create(self):
        user_dict = {
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
        student = Student.create(User.from_dict(user_dict))
        expect = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.assertEqual(student.to_dict(), expect)

    def test_approve(self):
        student_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.assertEqual(
            Student.from_dict(student_dict).approve().to_dict(), {
                **student_dict, 'join_status': 'approved'
            })


class StudentListTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dict(self):
        student_list = [{
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }, {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af392',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }]
        self.assertEqual(
            StudentList.from_list(student_list).to_list(), student_list)
