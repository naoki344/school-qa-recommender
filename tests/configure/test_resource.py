from unittest import TestCase
from unittest.mock import MagicMock

from app.configure.resoruce.cognito import create_cognito_client
from app.configure.resoruce.cognito import user_datasource
from app.configure.resoruce.dynamodb import classmate_datasource
from app.configure.resoruce.dynamodb import classmate_invite_datasource
from app.configure.resoruce.dynamodb import classroom_datasource
from app.configure.resoruce.dynamodb import create_dynamodb_client
from app.configure.resoruce.dynamodb import question_datasource
from app.configure.resoruce.dynamodb import sequences_datasource
from app.configure.resoruce.dynamodb import work_comment_datasource
from app.configure.resoruce.dynamodb import work_datasource
from app.configure.resoruce.s3 import create_s3_file_client
from app.dataaccess.aws.cognito import CognitoClient
from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.aws.s3_file import S3FileClient
from app.dataaccess.dynamodb.classroom import ClassmateDatasource
from app.dataaccess.dynamodb.classroom import ClassmateInviteDatasource
from app.dataaccess.dynamodb.classroom import ClassroomDatasource
from app.dataaccess.dynamodb.comment import WorkCommentDatasource
from app.dataaccess.dynamodb.question import QuestionDatasource
from app.dataaccess.dynamodb.question import SequensesDatasource
from app.dataaccess.dynamodb.work import WorkDatasource
from app.dataaccess.user import UserDatasource


class ResourceConfigureTest(TestCase):
    def test_run(self):
        self.assertEqual(
            isinstance(create_cognito_client(logger=MagicMock()),
                       CognitoClient), True)

        self.assertEqual(
            isinstance(user_datasource(logger=MagicMock()), UserDatasource),
            True)

        self.assertEqual(
            isinstance(create_dynamodb_client('test', logger=MagicMock()),
                       DynamoDBClient), True)

        self.assertEqual(
            isinstance(sequences_datasource(logger=MagicMock()),
                       SequensesDatasource), True)

        self.assertEqual(
            isinstance(question_datasource(logger=MagicMock()),
                       QuestionDatasource), True)

        self.assertEqual(
            isinstance(classroom_datasource(logger=MagicMock()),
                       ClassroomDatasource), True)

        self.assertEqual(
            isinstance(classmate_datasource(logger=MagicMock()),
                       ClassmateDatasource), True)

        self.assertEqual(
            isinstance(work_datasource(logger=MagicMock()), WorkDatasource),
            True)

        self.assertEqual(
            isinstance(work_comment_datasource(logger=MagicMock()),
                       WorkCommentDatasource), True)

        self.assertEqual(
            isinstance(create_s3_file_client('test', logger=MagicMock()),
                       S3FileClient), True)

        self.assertEqual(
            isinstance(classmate_invite_datasource(logger=MagicMock()),
                       ClassmateInviteDatasource), True)
