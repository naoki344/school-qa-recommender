from logging import Logger

from app.application.query.question import QuestionQueryService
from app.configure.resoruce.dynamodb import question_datasource


def question_query_service(logger: Logger) -> QuestionQueryService:
    return QuestionQueryService(question_datasource(logger), logger)
