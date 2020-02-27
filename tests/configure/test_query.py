from unittest import TestCase
from app.configure.query.user import user_query_service
from app.application.query.user import UserQueryService
from unittest.mock import MagicMock


class QueryConfigureTest(TestCase):
    def test_run(self):
        self.assertEqual(
            isinstance(user_query_service(logger=MagicMock()),
                       UserQueryService), True)
