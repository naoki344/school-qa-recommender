from unittest import TestCase
from unittest.mock import MagicMock

from app.configure.resoruce.cognito import create_cognito_client
from app.configure.resoruce.cognito import user_datasource
from app.configure.resoruce.dynamodb import class_room_datasource
from app.configure.resoruce.dynamodb import class_room_student_datasource
from app.configure.resoruce.dynamodb import create_dynamodb_client
from app.configure.resoruce.dynamodb import question_datasource
from app.configure.resoruce.dynamodb import sequences_datasource
from app.dataaccess.aws.cognito import CognitoClient
from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.class_room import ClassRoomDatasource
from app.dataaccess.dynamodb.class_room import ClassRoomStudentDatasource
from app.dataaccess.dynamodb.question import QuestionDatasource
from app.dataaccess.dynamodb.question import SequensesDatasource
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
            isinstance(class_room_datasource(logger=MagicMock()),
                       ClassRoomDatasource), True)

        self.assertEqual(
            isinstance(class_room_student_datasource(logger=MagicMock()),
                       ClassRoomStudentDatasource), True)
