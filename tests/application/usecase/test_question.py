from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock

import freezegun

from app.application.query.user import UserQueryService
from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import FindQuestion
from app.application.usecase.question import UpdateQuestion
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.model.user.user import User
from app.model.user.user import UserId


class CreateQuestionTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'question_answer': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'question_commentary': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_type': 'math',
            'question_type': 'selectable',
            'sort_tag_list': ['数学I', '初級']
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

    @freezegun.freeze_time('2020-02-11T20:20:18.033712+09:00')
    def test_run(self):
        # datasource の作成
        datasource = MagicMock()
        datasource.fetch_sequesnse_id = MagicMock(return_value=1)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        usecase = CreateQuestion(question_datasource=datasource,
                                 user_service=user_service,
                                 logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             item=deepcopy(self.question_dict))

        expect = {
            **self.question_dict, 'question_id': 1,
            'register_user_id': user_id.value,
            'register_user_name': 'Naoki'
        }
        datasource.fetch_sequesnse_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            Question.from_dict(expect))
        datasource.put_item.assert_not_called()
        user_service.find.assert_called_once_with(user_id)
        self.assertEqual(result.to_dict(), expect)


class UpdateQuestionTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'question_answer': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'question_commentary': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_type': 'math',
            'question_type': 'describing',
            'sort_tag_list': ['数学I', '初級']
        }

    def test_run_ok(self):
        datasource = MagicMock()
        usecase = UpdateQuestion(question_datasource=datasource,
                                 logger=MagicMock())
        result = usecase.run(QuestionId(1), deepcopy(self.question_dict))

        datasource.fetch_sequesnse_id.assert_not_called()
        datasource.put_item.assert_called_once_with(
            Question.from_dict(self.question_dict))
        self.assertEqual(result.to_dict(), self.question_dict)

    def test_run_mismutch_question_id(self):
        datasource = MagicMock()
        usecase = UpdateQuestion(question_datasource=datasource,
                                 logger=MagicMock())
        with self.assertRaises(Exception):
            usecase.run(QuestionId(2), deepcopy(self.question))


class FindQuestionTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'question_answer': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'question_commentary': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_type': 'math',
            'question_type': 'describing',
            'sort_tag_list': ['数学I', '初級']
        }

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Question.from_dict(self.question_dict))
        usecase = FindQuestion(question_datasource=datasource,
                               logger=MagicMock())
        result = usecase.run(QuestionId(1))

        datasource.find_by_id.assert_called_once_with(QuestionId(1))
        self.assertEqual(result.to_dict(), self.question_dict)
