from logging import Logger

from app.application.query.user import UserQueryService
from app.dataaccess.dynamodb.class_room import ClassRoomDatasource
from app.model.class_room.class_room import ClassRoom
from app.model.class_room.class_room import ClassRoomId
from app.model.user.user import UserId


class CreateClassRoom:
    def __init__(self, datasource: ClassRoomDatasource,
                 user_service: UserQueryService, logger: Logger) -> None:
        self.datasource = datasource
        self.user_service = user_service

    def run(self, user_id: UserId, item: dict) -> ClassRoom:
        _id = self.datasource.fetch_sequesnse_id()
        user = self.user_service.find(user_id)
        class_room = ClassRoom.create(_id, user, item)
        # TODO: validation
        self.datasource.insert_item(class_room)
        return class_room


class FindClassRoom:
    def __init__(self, datasource: ClassRoomDatasource,
                 logger: Logger) -> ClassRoom:
        self.datasource = datasource

    def run(self, class_room_id: ClassRoomId) -> ClassRoom:
        return self.datasource.find_by_id(class_room_id)
