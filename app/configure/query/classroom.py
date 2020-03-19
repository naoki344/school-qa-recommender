from logging import Logger

from app.application.query.classroom import ClassroomQueryService
from app.configure.resoruce.dynamodb import classroom_datasource


def classroom_query_service(logger: Logger) -> ClassroomQueryService:
    return ClassroomQueryService(classroom_datasource(logger), logger)
