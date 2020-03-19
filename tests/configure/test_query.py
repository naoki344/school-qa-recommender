from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.classroom import ClassroomQueryService
from app.application.query.question import QuestionQueryService
from app.application.query.user import UserQueryService
from app.configure.query.classroom import classroom_query_service
from app.configure.query.question import question_query_service
from app.configure.query.user import user_query_service


class QueryConfigureTest(TestCase):
    def test_run(self):
        self.assertEqual(
            isinstance(user_query_service(logger=MagicMock()),
                       UserQueryService), True)
        self.assertEqual(
            isinstance(question_query_service(logger=MagicMock()),
                       QuestionQueryService), True)
        self.assertEqual(
            isinstance(classroom_query_service(logger=MagicMock()),
                       ClassroomQueryService), True)
