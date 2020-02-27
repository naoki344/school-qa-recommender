from logging import Logger

from app.application.usecase.class_room import CreateClassRoom
from app.configure.query.user import user_query_service
from app.configure.resoruce.dynamodb import class_room_datasource


def create_class_room(logger: Logger) -> CreateClassRoom:
    datasource = class_room_datasource(logger=logger)
    user_service = user_query_service(logger)
    return CreateClassRoom(datasource=datasource,
                           user_service=user_service,
                           logger=logger)
