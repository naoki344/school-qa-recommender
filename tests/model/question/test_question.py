import freezegun
from unittest import TestCase
from app.model.question.question import Question
from app.model.question.question import QuestionCard
from datetime import datetime


class QuestionTest(TestCase):
    def test_dict_max(self):
        question_dict = {
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

        self.assertEqual(
            question_dict,
            Question.from_dict(question_dict).to_dict())

    @freezegun.freeze_time('2020-02-11T20:20:18.033712+09:00')
    def test_create(self):
        question_dict = {
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ??? テスト問題です。50文字で切り取られたsummaryを自動的に作成します。',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'},
            'question_answer': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'},
            'question_commentary': {
                'text': 'Question1 XXXX is ???',
                'image_url': 'https://xxxxxxxxxxxxxxx.jpg'},
            'subject_type': 'math',
            'question_type': 'describing',
            'sort_tag_list': [
                '数学I',
                '初級']}
        expect = {
            **question_dict,
            'question_id': 2,
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'question_sentence': {
                **question_dict['question_sentence'],
                'summary': 'Question1 XXXX is ??? テスト問題です。50文字で切り取られたsummaryを自'}}
        print(Question.create(2, question_dict).to_dict())
        self.assertEqual(
            expect,
            Question.create(2, question_dict).to_dict())

    def test_dict_min(self):
        question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'estimated_time': 15,
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
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
            'question_type': 'describing',
            'sort_tag_list': ['数学I', '初級']
        }

        self.assertEqual(
            question_dict,
            Question.from_dict(question_dict).to_dict())


class QuestionCardTest(TestCase):
    def test_dict_max(self):
        question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'text': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
                'image_url': None
            },
            'estimated_time': 15,
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_type': 'math',
            'question_type': 'selectable',
            'sort_tag_list': ['数学I', '初級']
        }
        self.assertEqual(
            question_dict,
            QuestionCard.from_db(question_dict).to_dict())
