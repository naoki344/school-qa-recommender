from unittest import TestCase
from app.model.question.question import Question


class QuestionTest(TestCase):
    def test_dict_min(self):
        question_dict = {
            'question_id': 1,
            'register_user_id': 30,
            'title': 'Test Question Title',
            'contents': 'Test Question Contents',
            # TODO: 日付フォーマットは後でかくにん
            'register_date': '2019-02-20 09:01:00.000+09:00',
            'subject_type': 'math',
            'caption': None
            }

        self.assertEqual(
            question_dict,
            Question.from_dict(question_dict).to_dict())

    def test_dict_max(self):
        question_dict = {
            'question_id': 1,
            'register_user_id': 30,
            'title': 'Test Question Title',
            'contents': 'Test Question Contents',
            # TODO: 日付フォーマットは後でかくにん
            'register_date': '2019-02-20 09:01:00.000+09:00',
            'subject_type': 'math',
            'caption': 'caption'
            }

        self.assertEqual(
            question_dict,
            Question.from_dict(question_dict).to_dict())
