from copy import deepcopy
from unittest import TestCase
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import UpdateQuestion
from app.application.usecase.question import FindQuestion
from unittest.mock import MagicMock


class CreateQuestionTest(TestCase):
    def test_run(self):
        question_dict = {
            'register_user_id': 30,
            'title': 'Test Question Title',
            'contents': 'Test Question Contents',
            # TODO: 日付フォーマットは後でかくにん
            'register_date': '2019-02-20 09:01:00.000+09:00',
            'subject_type': 'math',
            'caption': None
            }
        datasource = MagicMock()
        datasource.fetch_sequesnse_id = MagicMock(return_value=1)
        usecase = CreateQuestion(
            question_datasource=datasource, logger=MagicMock())
        result = usecase.run(deepcopy(question_dict))

        expect = {
            'question_id': 1,
            **question_dict
        }
        datasource.fetch_sequesnse_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            Question.from_dict(expect))
        datasource.put_item.assert_not_called()
        self.assertEqual(result.to_dict(), expect)


class UpdateQuestionTest(TestCase):
    def test_run_ok(self):
        question = {
            'question_id': 1,
            'register_user_id': 30,
            'title': 'Test Question Title',
            'contents': 'Test Question Contents',
            # TODO: 日付フォーマットは後でかくにん
            'register_date': '2019-02-20 09:01:00.000+09:00', 'subject_type': 'math',
            'caption': None
            }
        datasource = MagicMock()
        usecase = UpdateQuestion(
            question_datasource=datasource, logger=MagicMock())
        result = usecase.run(QuestionId(1), deepcopy(question))

        datasource.fetch_sequesnse_id.assert_not_called()
        datasource.put_item.assert_called_once_with(
            Question.from_dict(question))
        self.assertEqual(result.to_dict(), question)

    def test_run_mismutch_question_id(self):
        question = {
            'question_id': 1,
            'register_user_id': 30,
            'title': 'Test Question Title',
            'contents': 'Test Question Contents',
            # TODO: 日付フォーマットは後でかくにん
            'register_date': '2019-02-20 09:01:00.000+09:00', 'subject_type': 'math',
            'caption': None
            }
        datasource = MagicMock()
        usecase = UpdateQuestion(
            question_datasource=datasource, logger=MagicMock())
        with self.assertRaises(Exception):
            usecase.run(QuestionId(2), deepcopy(question))

class FindQuestionTest(TestCase):
    def test_run_ok(self):
        question = {
            'question_id': 1,
            'register_user_id': 30,
            'title': 'Test Question Title',
            'contents': 'Test Question Contents',
            # TODO: 日付フォーマットは後でかくにん
            'register_date': '2019-02-20 09:01:00.000+09:00',
            'subject_type': 'math',
            'caption': None
            }
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=Question.from_dict(question))
        usecase = FindQuestion(
            question_datasource=datasource, logger=MagicMock())
        result = usecase.run(QuestionId(1))

        datasource.find_by_id.assert_called_once_with(QuestionId(1))
        self.assertEqual(result.to_dict(), question)
