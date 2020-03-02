import os
from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.aws.dynamodb import TableResource
from app.dataaccess.dynamodb.class_room import ClassRoomDatasource
from app.dataaccess.dynamodb.class_room import ClassRoomStudentDatasource
from app.dataaccess.dynamodb.question import QuestionDatasource
from app.dataaccess.dynamodb.question import SequensesDatasource

stage_name = os.environ['STAGE_NAME']


def create_dynamodb_client(table_name: str, logger: Logger) -> DynamoDBClient:
    return DynamoDBClient(TableResource.create(table_name), logger)


def sequences_datasource(logger: Logger) -> SequensesDatasource:
    return SequensesDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-Sequenses', logger),
                               logger=logger)


def question_datasource(logger: Logger) -> QuestionDatasource:
    return QuestionDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-Question', logger),
                              sequenses_table=sequences_datasource(logger),
                              logger=logger)


def class_room_datasource(logger: Logger) -> ClassRoomDatasource:
    return ClassRoomDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-ClassRoom', logger),
                               sequenses_table=sequences_datasource(logger),
                               logger=logger)


def class_room_student_datasource(
        logger: Logger) -> ClassRoomStudentDatasource:
    return ClassRoomStudentDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-ClassRoomStudent', logger),
                                      logger=logger)
