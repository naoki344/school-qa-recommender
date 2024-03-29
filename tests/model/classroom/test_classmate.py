from unittest import TestCase

from app.model.classroom.classmate import Classmate
from app.model.classroom.classmate import ClassmateList
from app.model.user.user import User


class ClassmateTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dict(self):
        classmate_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.assertEqual(
            Classmate.from_dict(classmate_dict).to_dict(), classmate_dict)

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
        classmate = Classmate.create(User.from_dict(user_dict))
        expect = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.assertEqual(classmate.to_dict(), expect)

    def test_approve(self):
        classmate_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'email': 'trombone344@gmail.com',
            'join_status': 'requested'
        }
        self.assertEqual(
            Classmate.from_dict(classmate_dict).approve().to_dict(), {
                **classmate_dict, 'join_status': 'approved'
            })


class ClassmateListTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dict(self):
        classmate_list = [{
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
            ClassmateList.from_list(classmate_list).to_list(), classmate_list)

    def test_approved_only(self):
        classmate_list = [{
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
        self.assertEqual(
            ClassmateList.from_list(classmate_list).approved_only().to_list(),
            [classmate_list[1]])
