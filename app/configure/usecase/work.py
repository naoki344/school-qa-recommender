from logging import Logger

from app.application.usecase.work import CreateWorkFromQuestion
from app.application.usecase.work import GetClassroomWorkList
from app.configure.query.classroom import classroom_query_service
from app.configure.query.question import question_query_service
from app.configure.query.user import user_query_service
from app.configure.resoruce.dynamodb import work_datasource


def create_work_from_question(logger: Logger) -> CreateWorkFromQuestion:
    datasource = work_datasource(logger=logger)
    user_service = user_query_service(logger)
    classroom_serice = classroom_query_service(logger)
    return CreateWorkFromQuestion(
        work_datasource=datasource,
        question_serice=question_query_service(logger),
        classroom_serice=classroom_serice,
        user_service=user_service,
        logger=logger)


def get_classroom_work_list(logger: Logger) -> CreateWorkFromQuestion:
    datasource = work_datasource(logger=logger)
    user_service = user_query_service(logger)
    return GetClassroomWorkList(work_datasource=datasource,
                                user_service=user_service,
                                logger=logger)
