import os
from logging import Logger

from app.dataaccess.aws.cognito import CognitoClient
from app.dataaccess.user import UserDatasource

user_pool_id = os.environ['COGNITO_USER_POOL_ID']


def create_cognito_client(logger: Logger) -> CognitoClient:
    return CognitoClient(user_pool_id, logger)


def user_datasource(logger: Logger) -> UserDatasource:
    return UserDatasource(create_cognito_client(logger), logger)
