from unittest import TestCase

import freezegun

from app.model.comment.comment import WorkComment
from app.model.comment.comment import WorkCommentList
from app.model.user.user import User
from app.model.work.work import WorkId


class WorkCommentTest(TestCase):
    def test_dict(self):
        comment_dict = {
            'comment_id': 10,
            'comment_type': 'message',
            'parent_comment_id': 2,
            'work_id': 10,
            'body': 'comment body test',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.assertEqual(comment_dict,
                         WorkComment.from_dict(comment_dict).to_dict())

    def test_dict_min(self):
        comment_dict = {
            'comment_id': 10,
            'comment_type': 'topic',
            'work_id': 10,
            'body': 'comment body test',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.assertEqual({
            **comment_dict, 'parent_comment_id': None
        },
                         WorkComment.from_dict(comment_dict).to_dict())

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

        comment = WorkComment.create(work_id=WorkId(10),
                                     user=user,
                                     _id=10,
                                     comment_type='message',
                                     parent_comment_id=2,
                                     body='comment body test')

        comment_dict = {
            'comment_id': 10,
            'comment_type': 'message',
            'parent_comment_id': 2,
            'work_id': 10,
            'body': 'comment body test',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.assertEqual(comment_dict, comment.to_dict())


class WorkCommentListTest(TestCase):
    def test_dict(self):
        comment_list = [
            {
                'comment_id': 102,
                'comment_type': 'message',
                'parent_comment_id': None,
                'work_id': 10,
                'body': 'comment body test',
                'register_date': '2020-02-22T00:18:16.874000+09:00',
                'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'register_user_name': 'Naoki',
            },
            {
                'comment_id': 100,
                'comment_type': 'message',
                'parent_comment_id': None,
                'work_id': 10,
                'body': 'comment body test',
                'register_date': '2020-02-20T00:18:16.874000+09:00',
                'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'register_user_name': 'Naoki',
            },
            {
                'comment_id': 101,
                'comment_type': 'topic',
                'parent_comment_id': None,
                'work_id': 10,
                'body': 'comment body test',
                'register_date': '2020-02-21T00:18:16.874000+09:00',
                'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'register_user_name': 'Naoki',
            },
            {
                'comment_id': 104,
                'comment_type': 'message',
                'parent_comment_id': 101,
                'work_id': 10,
                'body': 'comment body test',
                'register_date': '2020-02-24T00:18:16.874000+09:00',
                'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'register_user_name': 'Naoki',
            },
            {
                'comment_id': 103,
                'comment_type': 'message',
                'parent_comment_id': 101,
                'work_id': 10,
                'body': 'comment body test',
                'register_date': '2020-02-23T00:18:16.874000+09:00',
                'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'register_user_name': 'Naoki',
            },
        ]
        expect = {
            "root_message_list": [
                {
                    'comment_id': 100,
                    'comment_type': 'message',
                    'parent_comment_id': None,
                    'work_id': 10,
                    'body': 'comment body test',
                    'register_date': '2020-02-20T00:18:16.874000+09:00',
                    'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                    'register_user_name': 'Naoki',
                },
                {
                    'comment_id': 102,
                    'comment_type': 'message',
                    'parent_comment_id': None,
                    'work_id': 10,
                    'body': 'comment body test',
                    'register_date': '2020-02-22T00:18:16.874000+09:00',
                    'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                    'register_user_name': 'Naoki',
                },
            ],
            "topic_list": [
                {
                    'comment_id': 101,
                    'comment_type': 'topic',
                    'parent_comment_id': None,
                    'work_id': 10,
                    'body': 'comment body test',
                    'register_date': '2020-02-21T00:18:16.874000+09:00',
                    'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                    'register_user_name': 'Naoki',
                },
            ],
            "topic_message_dict": {
                101: [
                    {
                        'comment_id': 103,
                        'comment_type': 'message',
                        'parent_comment_id': 101,
                        'work_id': 10,
                        'body': 'comment body test',
                        'register_date': '2020-02-23T00:18:16.874000+09:00',
                        'register_user_id':
                        '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                        'register_user_name': 'Naoki',
                    },
                    {
                        'comment_id': 104,
                        'comment_type': 'message',
                        'parent_comment_id': 101,
                        'work_id': 10,
                        'body': 'comment body test',
                        'register_date': '2020-02-24T00:18:16.874000+09:00',
                        'register_user_id':
                        '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                        'register_user_name': 'Naoki',
                    },
                ]
            },
        }
        self.maxDiff = None
        self.assertEqual(expect,
                         WorkCommentList.from_list(comment_list).to_response())
        expect = {
            "root_message_list": [],
            "topic_list": [],
            "topic_message_dict": {}
        }
        self.assertEqual(expect, WorkCommentList.from_list([]).to_response())
