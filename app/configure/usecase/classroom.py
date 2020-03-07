from logging import Logger

from app.application.usecase.classroom import ApproveJoinClassroomRequest
from app.application.usecase.classroom import CreateClassroom
from app.application.usecase.classroom import FindClassroom
from app.application.usecase.classroom import GetMyClassroomList
from app.application.usecase.classroom import RequestJoinClassroom
from app.configure.query.user import user_query_service
from app.configure.resoruce.dynamodb import classmate_datasource
from app.configure.resoruce.dynamodb import classroom_datasource


def create_classroom(logger: Logger) -> CreateClassroom:
    datasource = classroom_datasource(logger=logger)
    classmate = classmate_datasource(logger=logger)
    user_service = user_query_service(logger)
    return CreateClassroom(datasource=datasource,
                           classmate_datasource=classmate,
                           user_service=user_service,
                           logger=logger)


def find_classroom(logger: Logger) -> FindClassroom:
    datasource = classroom_datasource(logger=logger)
    classmate = classmate_datasource(logger=logger)
    user_service = user_query_service(logger)
    return FindClassroom(datasource=datasource,
                         classmate_datasource=classmate,
                         user_service=user_service,
                         logger=logger)


def request_join_classroom(logger: Logger) -> RequestJoinClassroom:
    datasource = classroom_datasource(logger=logger)
    classmate = classmate_datasource(logger=logger)
    user_service = user_query_service(logger)
    return RequestJoinClassroom(datasource=datasource,
                                classmate_datasource=classmate,
                                user_service=user_service,
                                logger=logger)


def approve_join_classroom_request(
        logger: Logger) -> ApproveJoinClassroomRequest:
    datasource = classroom_datasource(logger=logger)
    classmate = classmate_datasource(logger=logger)
    user_service = user_query_service(logger)
    return ApproveJoinClassroomRequest(datasource=datasource,
                                       classmate_datasource=classmate,
                                       user_service=user_service,
                                       logger=logger)


def get_my_classroom_list(logger: Logger) -> FindClassroom:
    datasource = classroom_datasource(logger=logger)
    classmate = classmate_datasource(logger=logger)
    user_service = user_query_service(logger)
    return GetMyClassroomList(datasource=datasource,
                              classmate_datasource=classmate,
                              user_service=user_service,
                              logger=logger)
