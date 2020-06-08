from unittest import TestCase

from app.model.classroom.classroom import Classroom
from app.model.user.user import User


class ClassroomTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dict_max(self):
        class_dict = {
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
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
        self.assertEqual(Classroom.from_dict(class_dict).to_dict(), class_dict)

    def test_dict_min(self):
        class_dict = {
            'classroom_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'private',
            'tag_list': ['tag1', 'tag2']
        }
        self.assertEqual(
            Classroom.from_dict(class_dict).to_dict(), {
                **class_dict, 'capacity': None,
                'caption': None
            })

    def test_dict_create(self):
        class_dict = {
            'name': 'test name',
            'image_url': 'https://example.example.com/test.jpg',
            'publish_type': 'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity': 10,
            'caption': 'test caption'
        }
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
        user = User.from_dict(user_dict)
        expect = {
            **class_dict, 'classroom_id':
            2,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
                'email': 'trombone344@gmail.com'
            }]
        }
        self.assertEqual(expect,
                         Classroom.create(2, user, class_dict).to_dict())
