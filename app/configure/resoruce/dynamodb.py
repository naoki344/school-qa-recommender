import os
from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.aws.dynamodb import TableResource
from app.dataaccess.dynamodb.question import QuestionDatasource
from app.dataaccess.dynamodb.question import SequensesDatasource
from app.dataaccess.dynamodb.class_room import ClassRoomDatasource

stage_name = os.environ['STAGE_NAME']


def create_dynamodb_client(table_name: str, logger: Logger) -> DynamoDBClient:
    return DynamoDBClient(TableResource.create(table_name), logger)


def sequences_datasource(logger: Logger) -> SequensesDatasource:
    return SequensesDatasource(client=create_dynamodb_client(
        f'{stage_name}-qa-Sequenses', logger),
                               logger=logger)


def question_datasource(logger: Logger) -> QuestionDatasource:
    return QuestionDatasource(client=create_dynamodb_client(
        f'{stage_name}-qa-Question', logger),
                              sequenses_table=sequences_datasource(logger),
                              logger=logger)


def class_room_datasource(logger: Logger) -> ClassRoomDatasource:
    return ClassRoomDatasource(client=create_dynamodb_client(
        f'{stage_name}-qa-ClassRoom', logger),
                              sequenses_table=sequences_datasource(logger),
                              logger=logger)
