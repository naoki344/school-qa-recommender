from unittest import TestCase
from unittest.mock import MagicMock

import freezegun

from app.application.query.classroom import ClassroomQueryService
from app.application.query.user import UserQueryService
from app.application.query.work import WorkQueryService
from app.application.usecase.comment import GetWorkCommentList
from app.application.usecase.comment import RegisterWorkComment
from app.dataaccess.dynamodb.work import WorkDatasource
from app.model.classroom.classroom import ClassroomId
from app.model.comment.comment import WorkComment
from app.model.comment.comment import WorkCommentList
from app.model.user.user import User
from app.model.user.user import UserId
from app.model.work.work import Work
from app.model.work.work import WorkId


class RegisterWorkCommentTest(TestCase):
    def setUp(self):
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
        self.work_dict = {
            'work_id': 1,
            'work_type': 'discussion',
            'classroom_id': 20,
            'title': 'work title test',
            'caption': 'caption test',
            'origin_id': 1,
            'origin_type': 'question',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.work = Work.from_dict(self.work_dict)

    @freezegun.freeze_time('2020-02-26T00:18:16.874000+09:00')
    def test_run(self):
        # datasource の作成
        datasource = MagicMock(spec=WorkDatasource)
        datasource.fetch_sequense_id = MagicMock(return_value=100)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        classroom_service = MagicMock(spec=ClassroomQueryService)
        work_service = MagicMock(spec=WorkQueryService)
        work_service.find = MagicMock(return_value=self.work)

        usecase = RegisterWorkComment(comment_datasource=datasource,
                                      work_service=work_service,
                                      classroom_service=classroom_service,
                                      user_service=user_service,
                                      logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             classroom_id=ClassroomId(20),
                             work_id=WorkId(5),
                             data={
                                 'parent_comment_id': 2,
                                 'body': 'commend body',
                                 'comment_type': 'message',
                             })

        expect = {
            'comment_id': 100,
            'comment_type': 'message',
            'work_id': 5,
            'parent_comment_id': 2,
            'body': 'commend body',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        datasource.fetch_sequense_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            WorkComment.from_dict(expect))
        user_service.find.assert_called_once_with(user_id)
        self.assertEqual(result.to_dict(), expect)


class GetWorkCommentListTest(TestCase):
    def setUp(self):
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
        self.work_dict = {
            'work_id': 1,
            'work_type': 'discussion',
            'classroom_id': 20,
            'title': 'work title test',
            'caption': 'caption test',
            'origin_id': 1,
            'origin_type': 'question',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'register_user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'register_user_name': 'Naoki',
        }
        self.work = Work.from_dict(self.work_dict)
        self.comment_list = [
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

    @freezegun.freeze_time('2020-02-26T00:18:16.874000+09:00')
    def test_run(self):
        expect = WorkCommentList.from_list(self.comment_list)
        # datasource の作成
        datasource = MagicMock(spec=WorkDatasource)
        datasource.find_by_work_id = MagicMock(return_value=expect)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        classroom_service = MagicMock(spec=ClassroomQueryService)
        work_service = MagicMock(spec=WorkQueryService)
        work_service.find = MagicMock(return_value=self.work)

        usecase = GetWorkCommentList(comment_datasource=datasource,
                                     work_service=work_service,
                                     classroom_service=classroom_service,
                                     user_service=user_service,
                                     logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             classroom_id=ClassroomId(20),
                             work_id=WorkId(5))

        user_service.find.assert_called_once_with(user_id)
        work_service.find.assert_called_once_with(WorkId(5))
        datasource.find_by_work_id.assert_called_once_with(WorkId(5))
        self.assertEqual(result.to_response(), expect.to_response())
