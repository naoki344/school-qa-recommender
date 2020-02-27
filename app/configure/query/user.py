from logging import Logger

from app.application.query.user import UserQueryService
from app.configure.resoruce.cognito import user_datasource


def user_query_service(logger: Logger) -> UserQueryService:
    return UserQueryService(user_datasource(logger), logger)
