import os
from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.aws.dynamodb import TableResource
from app.dataaccess.dynamodb.classroom import ClassmateDatasource
from app.dataaccess.dynamodb.classroom import ClassroomDatasource
from app.dataaccess.dynamodb.comment import WorkCommentDatasource
from app.dataaccess.dynamodb.question import QuestionDatasource
from app.dataaccess.dynamodb.question import SequensesDatasource
from app.dataaccess.dynamodb.work import WorkDatasource

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


def classroom_datasource(logger: Logger) -> ClassroomDatasource:
    return ClassroomDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-Classroom', logger),
                               sequenses_table=sequences_datasource(logger),
                               logger=logger)


def classmate_datasource(logger: Logger) -> ClassmateDatasource:
    return ClassmateDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-Classmate', logger),
                               logger=logger)


def work_datasource(logger: Logger) -> WorkDatasource:
    return WorkDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-Work', logger),
                          sequenses_table=sequences_datasource(logger),
                          logger=logger)


def work_comment_datasource(logger: Logger) -> WorkCommentDatasource:
    return WorkCommentDatasource(client=create_dynamodb_client(
        f'{stage_name}-tt-WorkComment', logger),
                                 sequenses_table=sequences_datasource(logger),
                                 logger=logger)
