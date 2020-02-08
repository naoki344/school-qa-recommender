from logging import Logger

from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import UpdateQuestion
from app.application.usecase.question import FindQuestion
from app.configure.resoruce.dynamodb import question_datasource


def create_question(stage_name: str, logger: Logger) -> CreateQuestion:
    datasource = question_datasource(
        stage_name, logger=logger)
    return CreateQuestion(
        question_datasource=datasource, logger=logger)


def update_question(stage_name: str, logger: Logger) -> UpdateQuestion:
    datasource = question_datasource(
        stage_name, logger=logger)
    return UpdateQuestion(
        question_datasource=datasource, logger=logger)


def find_question(stage_name: str, logger: Logger) -> CreateQuestion:
    datasource = question_datasource(
        stage_name, logger=logger)
    return FindQuestion(
        question_datasource=datasource, logger=logger)
