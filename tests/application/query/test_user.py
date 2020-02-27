from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock

import freezegun

from app.application.query.user import UserQueryService
from app.model.user.user import User
from app.model.user.user import UserId


class UserQueryServiceTest(TestCase):
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

    def test_find(self):
        user_datasource = MagicMock()
        user_datasource.find = MagicMock(return_value=self.user)
        service = UserQueryService(user_datasource, MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = service.find(user_id)
        self.assertEqual(result, self.user)
        user_datasource.find.assert_called_once_with(user_id)
