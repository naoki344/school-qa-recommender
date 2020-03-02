from logging import Logger

from app.application.usecase.class_room import ApproveJoinClassRoomRequest
from app.application.usecase.class_room import CreateClassRoom
from app.application.usecase.class_room import FindClassRoom
from app.application.usecase.class_room import RequestJoinClassRoom
from app.configure.query.user import user_query_service
from app.configure.resoruce.dynamodb import class_room_datasource
from app.configure.resoruce.dynamodb import class_room_student_datasource


def create_class_room(logger: Logger) -> CreateClassRoom:
    datasource = class_room_datasource(logger=logger)
    user_service = user_query_service(logger)
    return CreateClassRoom(datasource=datasource,
                           user_service=user_service,
                           logger=logger)


def find_class_room(logger: Logger) -> FindClassRoom:
    datasource = class_room_datasource(logger=logger)
    student_datasource = class_room_student_datasource(logger=logger)
    return FindClassRoom(datasource=datasource,
                         student_datasource=student_datasource,
                         logger=logger)


def request_join_class_room(logger: Logger) -> RequestJoinClassRoom:
    datasource = class_room_datasource(logger=logger)
    student_datasource = class_room_student_datasource(logger=logger)
    user_service = user_query_service(logger)
    return RequestJoinClassRoom(datasource=datasource,
                                student_datasource=student_datasource,
                                user_service=user_service,
                                logger=logger)


def approve_join_class_room_request(
        logger: Logger) -> ApproveJoinClassRoomRequest:
    datasource = class_room_datasource(logger=logger)
    student_datasource = class_room_student_datasource(logger=logger)
    user_service = user_query_service(logger)
    return ApproveJoinClassRoomRequest(datasource=datasource,
                                       student_datasource=student_datasource,
                                       user_service=user_service,
                                       logger=logger)
