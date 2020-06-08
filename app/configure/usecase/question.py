from logging import Logger

from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import FindQuestion
from app.application.usecase.question import GetQuestionList
from app.application.usecase.question import UpdateQuestion
from app.configure.query.user import user_query_service
from app.configure.resoruce.dynamodb import question_datasource


def create_question(logger: Logger) -> CreateQuestion:
    datasource = question_datasource(logger=logger)
    user_service = user_query_service(logger)
    return CreateQuestion(question_datasource=datasource,
                          user_service=user_service,
                          logger=logger)


def update_question(logger: Logger) -> UpdateQuestion:
    datasource = question_datasource(logger=logger)
    return UpdateQuestion(question_datasource=datasource, logger=logger)


def find_question(logger: Logger) -> CreateQuestion:
    datasource = question_datasource(logger=logger)
    return FindQuestion(question_datasource=datasource, logger=logger)


def get_question_list(logger: Logger) -> CreateQuestion:
    datasource = question_datasource(logger=logger)
    return GetQuestionList(question_datasource=datasource, logger=logger)
