from unittest import TestCase

from app.model.classroom.owner import ClassroomOwnerList
from app.model.user.user import UserId


class ClassroomOwnerListTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_is_owner(self):
        owner_list = ClassroomOwnerList.from_list([{
            'user_id':
            '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname':
            'Naoki',
            'email':
            'trombone344@gmail.com',
        }, {
            'user_id':
            '79434f7e-b53f-4d3a-8c79-aedc7b73af39-2',
            'nickname':
            'Naoki',
            'email':
            'trombone344@gmail.com',
        }])

        self.assertEqual(
            owner_list.is_owner(
                UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')), True)

        self.assertEqual(
            owner_list.is_owner(
                UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39-11')), False)
