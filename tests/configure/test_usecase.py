from unittest import TestCase
from unittest.mock import MagicMock

from app.application.usecase.user import UploadUserAvatarImage
from app.application.query.user import UserQueryService
from app.application.usecase.classroom import ApproveJoinClassroomRequest
from app.application.usecase.classroom import CreateClassroom
from app.application.usecase.classroom import FindClassroom
from app.application.usecase.classroom import GetMyClassroomList
from app.application.usecase.classroom import RequestJoinClassroom
from app.application.usecase.comment import GetWorkCommentList
from app.application.usecase.comment import RegisterWorkComment
from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import FindQuestion
from app.application.usecase.question import GetQuestionList
from app.application.usecase.question import UpdateQuestion
from app.application.usecase.work import CreateWorkFromQuestion
from app.application.usecase.work import FindClassroomWork
from app.application.usecase.work import GetClassroomWorkList
from app.configure.usecase.classroom import approve_join_classroom_request
from app.configure.usecase.classroom import create_classroom
from app.configure.usecase.classroom import find_classroom
from app.configure.usecase.classroom import get_my_classroom_list
from app.configure.usecase.classroom import request_join_classroom
from app.configure.usecase.comment import get_work_comment_list
from app.configure.usecase.comment import register_work_comment
from app.configure.usecase.question import create_question
from app.configure.usecase.question import find_question
from app.configure.usecase.question import get_question_list
from app.configure.usecase.question import update_question
from app.configure.usecase.work import create_work_from_question
from app.configure.usecase.work import find_classroom_work
from app.configure.usecase.work import get_classroom_work_list
from app.configure.usecase.user import upload_user_avatar_image


class QuestionUsecaseTest(TestCase):
    def test_run(self):
        self.assertEqual(
            isinstance(create_question(logger=MagicMock()), CreateQuestion),
            True)

        self.assertEqual(
            isinstance(update_question(logger=MagicMock()), UpdateQuestion),
            True)

        self.assertEqual(
            isinstance(find_question(logger=MagicMock()), FindQuestion), True)

        self.assertEqual(
            isinstance(get_question_list(logger=MagicMock()), GetQuestionList),
            True)

        self.assertEqual(
            isinstance(create_classroom(logger=MagicMock()), CreateClassroom),
            True)

        self.assertEqual(
            isinstance(find_classroom(logger=MagicMock()), FindClassroom),
            True)

        self.assertEqual(
            isinstance(request_join_classroom(logger=MagicMock()),
                       RequestJoinClassroom), True)

        self.assertEqual(
            isinstance(approve_join_classroom_request(logger=MagicMock()),
                       ApproveJoinClassroomRequest), True)

        self.assertEqual(
            isinstance(get_my_classroom_list(logger=MagicMock()),
                       GetMyClassroomList), True)

        self.assertEqual(
            isinstance(create_work_from_question(logger=MagicMock()),
                       CreateWorkFromQuestion), True)

        self.assertEqual(
            isinstance(get_classroom_work_list(logger=MagicMock()),
                       GetClassroomWorkList), True)

        self.assertEqual(
            isinstance(find_classroom_work(logger=MagicMock()),
                       FindClassroomWork), True)

        self.assertEqual(
            isinstance(register_work_comment(logger=MagicMock()),
                       RegisterWorkComment), True)

        self.assertEqual(
            isinstance(get_work_comment_list(logger=MagicMock()),
                       GetWorkCommentList), True)

        self.assertEqual(
            isinstance(upload_user_avatar_image(logger=MagicMock()),
                       UploadUserAvatarImage), True)
