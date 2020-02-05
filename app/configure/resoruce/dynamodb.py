from logging import Logger
from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.aws.dynamodb import TableResource
from app.dataaccess.dynamodb.question import \
    QuestionDatasource


def create_dynamodb_client(
        table_name: str, logger: Logger) -> DynamoDBClient:
    return DynamoDBClient(
        TableResource.create(table_name), logger)


def question_datasource(
        stage_name: str,
        logger: Logger) -> QuestionDatasource:
    return QuestionDatasource(
        client=create_dynamodb_client(f'{stage_name}-qa-Question', logger),
        logger=logger)
