from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.sequences import SequensesDatasource
from app.model.class_room.class_room import ClassRoom
from app.model.class_room.class_room import ClassRoomId


class ClassRoomDatasource:
    def __init__(self, client: DynamoDBClient,
                 sequenses_table: SequensesDatasource, logger: Logger) -> None:
        self.client = client
        self.sequenses_table = sequenses_table
        self.logger = logger

    def insert_item(self, item: ClassRoom) -> None:
        self.client.insert_item(item.to_dict(), "class_room_id")

    def put_item(self, item: ClassRoom) -> None:
        self.client.put_item(item.to_dict())

    def fetch_sequesnse_id(self) -> int:
        name = f"Dynamodb#{self.client.table.table_name}"
        _id = self.sequenses_table.fetch_sequense_id(name)
        return _id

    def find_by_id(self, class_room_id: ClassRoomId) -> ClassRoom:
        data = self.client.get_item({'class_room_id': class_room_id.value})
        return ClassRoom.from_dict(data)
