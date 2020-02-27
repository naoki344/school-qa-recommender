from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.user import UserQueryService
from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import FindQuestion
from app.application.usecase.question import GetQuestionList
from app.application.usecase.question import UpdateQuestion
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
