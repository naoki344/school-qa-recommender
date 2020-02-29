from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.user import UserQueryService
from app.application.usecase.class_room import ApproveJoinClassRoomRequest
from app.application.usecase.class_room import CreateClassRoom
from app.application.usecase.class_room import FindClassRoom
from app.application.usecase.class_room import RequestJoinClassRoom
from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import FindQuestion
from app.application.usecase.question import GetQuestionList
from app.application.usecase.question import UpdateQuestion
from app.configure.usecase.class_room import approve_join_class_room_request
from app.configure.usecase.class_room import create_class_room
from app.configure.usecase.class_room import find_class_room
from app.configure.usecase.class_room import request_join_class_room
from app.configure.usecase.question import create_question
from app.configure.usecase.question import find_question
from app.configure.usecase.question import get_question_list
from app.configure.usecase.question import update_question


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
            isinstance(create_class_room(logger=MagicMock()), CreateClassRoom),
            True)

        self.assertEqual(
            isinstance(find_class_room(logger=MagicMock()), FindClassRoom),
            True)

        self.assertEqual(
            isinstance(request_join_class_room(logger=MagicMock()),
                       RequestJoinClassRoom), True)

        self.assertEqual(
            isinstance(approve_join_class_room_request(logger=MagicMock()),
                       ApproveJoinClassRoomRequest), True)
