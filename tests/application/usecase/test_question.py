import freezegun
from copy import deepcopy
from unittest import TestCase
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import UpdateQuestion
from app.application.usecase.question import FindQuestion
from unittest.mock import MagicMock


class CreateQuestionTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
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
            'sort_tag_list': ['数学I', '初級']
            }

    @freezegun.freeze_time('2020-02-11T20:20:18.033712+09:00')
    def test_run(self):
        datasource = MagicMock()
        datasource.fetch_sequesnse_id = MagicMock(return_value=1)
        usecase = CreateQuestion(
            question_datasource=datasource, logger=MagicMock())
        result = usecase.run(deepcopy(self.question_dict))

        expect = {
            'question_id': 1,
            **self.question_dict
        }
        datasource.fetch_sequesnse_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            Question.from_dict(expect))
        datasource.put_item.assert_not_called()
        self.assertEqual(result.to_dict(), expect)


class UpdateQuestionTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
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
            'sort_tag_list': ['数学I', '初級']
            }

    def test_run_ok(self):
        datasource = MagicMock()
        usecase = UpdateQuestion(
            question_datasource=datasource, logger=MagicMock())
        result = usecase.run(QuestionId(1), deepcopy(self.question_dict))

        datasource.fetch_sequesnse_id.assert_not_called()
        datasource.put_item.assert_called_once_with(
            Question.from_dict(self.question_dict))
        self.assertEqual(result.to_dict(), self.question_dict)

    def test_run_mismutch_question_id(self):
        datasource = MagicMock()
        usecase = UpdateQuestion(
            question_datasource=datasource, logger=MagicMock())
        with self.assertRaises(Exception):
            usecase.run(QuestionId(2), deepcopy(self.question))

class FindQuestionTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
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
            'sort_tag_list': ['数学I', '初級']
            }

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Question.from_dict(self.question_dict))
        usecase = FindQuestion(
            question_datasource=datasource, logger=MagicMock())
        result = usecase.run(QuestionId(1))

        datasource.find_by_id.assert_called_once_with(QuestionId(1))
        self.assertEqual(result.to_dict(), self.question_dict)
