import freezegun
from unittest import TestCase
from app.model.question.question import Question
from datetime import datetime


class QuestionTest(TestCase):
    def test_dict_max(self):
        question_dict = {
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

        self.assertEqual(
            question_dict,
            Question.from_dict(question_dict).to_dict())

    @freezegun.freeze_time('2020-02-11T20:20:18.033712+09:00')
    def test_create(self):
        question_dict = {
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
            'subject_type': 'math',
            'sort_tag_list': ['数学I', '初級']
        }
        expect = {
            **question_dict,
            'question_id': 2,
            'register_date': '2020-02-11T20:20:18.033712+09:00',
        }
        print(Question.create(2, question_dict).to_dict())
        self.assertEqual(
            expect,
            Question.create(2, question_dict).to_dict())

    def test_dict_min(self):
        question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
                'image_url': None
            },
            'question_answer': {
                'text': 'Question1 XXXX is ???',
                'image_url': None
            },
            'question_commentary': {
                'text': 'Question1 XXXX is ???',
                'image_url': None
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_type': 'math',
            'sort_tag_list': ['数学I', '初級']
        }

        self.assertEqual(
            question_dict,
            Question.from_dict(question_dict).to_dict())
