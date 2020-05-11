from datetime import datetime
from unittest import TestCase

import freezegun

from app.model.question.question import Question
from app.model.question.question import QuestionCard
from app.model.user.user import User


class QuestionTest(TestCase):
    def test_dict_max(self):
        question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'contents': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???'
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_name': '数学',
            'question_type': 'discussion',
            'sort_tag_list': ['数学I', '初級']
        }

        self.assertEqual(question_dict,
                         Question.from_dict(question_dict).to_dict())

    @freezegun.freeze_time('2020-02-11T20:20:18.033712+09:00')
    def test_create(self):
        question_dict = {
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'contents':
                'Question1 XXXX is ??? テスト問題です。50文字で切り取られたsummaryを自動的に作成します。',
            },
            'subject_name': '数学',
            'question_type': 'describing',
            'sort_tag_list': ['数学I', '初級']
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
            **question_dict,
            'question_id': 2,
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'question_sentence': {
                **question_dict['question_sentence'], 'summary':
                'Question1 XXXX is ??? テスト問題です。50文字で切り取られたsummaryを自'
            },
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.assertEqual(expect,
                         Question.create(2, user, question_dict).to_dict())

    def test_dict_min(self):
        question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'contents': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_name': '数学',
            'question_type': 'describing',
            'sort_tag_list': ['数学I', '初級']
        }

        self.assertEqual(question_dict,
                         Question.from_dict(question_dict).to_dict())


class QuestionCardTest(TestCase):
    def test_dict_max(self):
        self.maxDiff = None
        question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'contents':
                '<a>Question1 XXXX is ???</a><img src="./image_url.png" />',
                'summary': 'Question1 XXXX is ???'
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_name': '数学',
            'question_type': 'selectable',
            'sort_tag_list': ['数学I', '初級']
        }
        self.assertEqual({
            **question_dict, 'image_url': './image_url.png'
        },
                         QuestionCard.from_db(question_dict).to_dict())
