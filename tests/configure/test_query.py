from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.user import UserQueryService
from app.configure.query.user import user_query_service


class QueryConfigureTest(TestCase):
    def test_run(self):
        self.assertEqual(
            isinstance(user_query_service(logger=MagicMock()),
                       UserQueryService), True)
