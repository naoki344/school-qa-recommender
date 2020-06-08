from unittest import TestCase

from app.anticorruption.model.user.parser import AuthenticationEventPerser
from app.anticorruption.model.user.parser import CognitoUserParser
from app.model.user.user import User
from app.model.user.user import UserId

from .data.cognito import create_cognito_user
from .data.lambda_event import create_lambda_event_dict


class AuthenticationEventPerserTest(TestCase):
    def test_parse(self):
        cognito_user_id = AuthenticationEventPerser.parse(
            create_lambda_event_dict())
        self.assertEqual(cognito_user_id,
                         UserId("79434f7e-b53f-4d3a-8c79-aedc7b73af39"))


class CognitoUserParserTest(TestCase):
    def test_parse(self):
        user = CognitoUserParser.parse(create_cognito_user())
        expect_user = User.from_dict({
            'user_id':
            '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname':
            'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email':
            'trombone344@gmail.com',
            'register_date':
            '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub':
            '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        })
        self.assertEqual(user, expect_user)
