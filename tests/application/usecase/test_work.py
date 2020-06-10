from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock

import freezegun

from app.application.query.classroom import ClassroomQueryService
from app.application.query.question import QuestionQueryService
from app.application.query.user import UserQueryService
from app.application.usecase.work import CreateWorkFromQuestion
from app.application.usecase.work import FindClassroomWork
from app.dataaccess.dynamodb.comment import WorkCommentDatasource
from app.dataaccess.dynamodb.work import WorkDatasource
from app.model.classroom.classroom import Classroom
from app.model.classroom.classroom import ClassroomId
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.model.user.user import User
from app.model.user.user import UserId
from app.model.work.work import Work
from app.model.work.work import WorkId


class CreateWorkFromQuestionTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'contents': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_name': 'math',
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
        self.classroom_dict = {
            'classroom_id':
            20,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39-1',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        }
        self.user = User.from_dict(self.user_dict)
        self.question = Question.from_dict(self.question_dict)
        self.classroom = Classroom.from_dict(self.classroom_dict)

    @freezegun.freeze_time('2020-02-26T00:18:16.874000+09:00')
    def test_run(self):
        # datasource の作成
        datasource = MagicMock(spec=WorkDatasource)
        datasource.fetch_sequense_id = MagicMock(return_value=1)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        question_service = MagicMock(spec=QuestionQueryService)
        question_service.find = MagicMock(return_value=self.question)

        classroom_service = MagicMock(spec=ClassroomQueryService)
        classroom_service.find = MagicMock(return_value=self.classroom)

        usecase = CreateWorkFromQuestion(
            work_datasource=datasource,
            comment_datasource=MagicMock(spec=WorkCommentDatasource),
            question_service=question_service,
            classroom_service=classroom_service,
            user_service=user_service,
            logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             classroom_id=ClassroomId(20),
                             data={
                                 'question_id': 1,
                                 'title': 'work title test',
                                 'caption': 'caption test'
                             })

        expect = {
            'work_id': 1,
            'work_type': 'discussion',
            'classroom_id': 20,
            'title': 'work title test',
            'caption': 'caption test',
            'image_url': 'work-default-image.png',
            'origin_id': 1,
            'origin_type': 'question',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        datasource.fetch_sequense_id.assert_called_once()
        datasource.insert_item.assert_called_once()
        user_service.find.assert_called_once_with(user_id)
        classroom_service.find.assert_called_once_with(ClassroomId(20))
        question_service.find.assert_called_once_with(QuestionId(1))
        self.assertEqual(result.to_dict(), expect)
        usecase.comment_datasource.fetch_sequense_id.assert_called_once()
        usecase.comment_datasource.insert_item.assert_called_once()


class FindClassroomWorkTest(TestCase):
    def setUp(self):
        self.question_dict = {
            'question_id': 1,
            'register_user_id': "fjeiwo0g-rfar-fae",
            'register_user_name': '三好直紀',
            'question_sentence': {
                'contents': 'Question1 XXXX is ???',
                'summary': 'Question1 XXXX is ???',
            },
            'register_date': '2020-02-11T20:20:18.033712+09:00',
            'subject_name': 'math',
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
        self.work_dict = {
            'work_id': 1,
            'work_type': 'discussion',
            'classroom_id': 20,
            'title': 'work title test',
            'caption': 'caption test',
            'image_url': None,
            'origin_id': 1,
            'origin_type': 'question',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.user = User.from_dict(self.user_dict)
        self.question = Question.from_dict(self.question_dict)
        self.work = Work.from_dict(self.work_dict)

    @freezegun.freeze_time('2020-02-26T00:18:16.874000+09:00')
    def test_run(self):
        # datasource の作成
        datasource = MagicMock(spec=WorkDatasource)
        datasource.find_by_id = MagicMock(return_value=self.work)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        question_service = MagicMock(spec=QuestionQueryService)
        question_service.find = MagicMock(return_value=self.question)

        classroom_service = MagicMock(spec=ClassroomQueryService)

        usecase = FindClassroomWork(work_datasource=datasource,
                                    question_service=question_service,
                                    classroom_service=classroom_service,
                                    user_service=user_service,
                                    logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             classroom_id=ClassroomId(20),
                             work_id=WorkId(1))

        datasource.find_by_id.assert_called_once_with(WorkId(1))
        user_service.find.assert_called_once_with(user_id)
        question_service.find.assert_called_once_with(QuestionId(1))
        self.assertEqual(result[0].to_dict(), self.work_dict)
        self.assertEqual(result[1].to_dict(), self.question_dict)
        self.assertEqual(result[2], [])
