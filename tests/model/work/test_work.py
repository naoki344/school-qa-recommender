from unittest import TestCase

import freezegun

from app.model.classroom.classroom import ClassroomId
from app.model.question.question import Question
from app.model.user.user import User
from app.model.work.work import Work


class WorkTest(TestCase):
    def test_dict(self):
        work_dict = {
            'work_id': 1,
            'work_type': 'discussion',
            'classroom_id': 20,
            'title': 'work title test',
            'caption': 'caption test',
            'image_url': 'Image Url test',
            'origin_id': 1,
            'origin_type': 'question',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.assertEqual(work_dict, Work.from_dict(work_dict).to_dict())

    @freezegun.freeze_time('2020-02-26T00:18:16.874000+09:00')
    def test_create_from_question(self):
        user = User.from_dict({
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
        question = Question.from_dict({
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'contents': '<a>Question1 XXXX is ???</a><img src="./image_url.png" />',
                'summary': 'Question1 XXXX is ???'
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_name': '数学I',
            'question_type': 'selectable',
            'sort_tag_list': ['数学I', '初級']
        })

        expect_dict = {
            'work_id': 1,
            'work_type': 'discussion',
            'classroom_id': 20,
            'title': 'work title test',
            'caption': 'caption test',
            'image_url': './image_url.png',
            'origin_id': 1,
            'origin_type': 'question',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        work = Work.create_from_question(1, ClassroomId(20), user, question,
                                         expect_dict)
        self.assertEqual(expect_dict, work.to_dict())
