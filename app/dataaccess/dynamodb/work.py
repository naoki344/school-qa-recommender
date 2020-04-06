from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.sequences import SequensesDatasource
from app.model.classroom.classroom import ClassroomId
from app.model.work.work import Work
from app.model.work.work import WorkId


class WorkDatasource:
    def __init__(self, client: DynamoDBClient,
                 sequenses_table: SequensesDatasource, logger: Logger) -> None:
        self.client = client
        self.sequenses_table = sequenses_table
        self.logger = logger

    def insert_item(self, item: Work) -> None:
        self.client.insert_item(item.to_dict(), "work_id")

    def fetch_sequense_id(self) -> int:
        name = f"Dynamodb#{self.client.table.table_name}"
        _id = self.sequenses_table.fetch_sequense_id(name)
        return _id

    def find_by_id(self, work_id: WorkId) -> Work:
        data = self.client.get_item({'work_id': work_id.value})
        if data:
            return Work.from_dict(data)
        raise Exception('Classroom not found.')

    def find_by_classroom_id(self, classroom_id: ClassroomId) -> Work:
        item_list = self.client.get_items(name='classroom_id',
                                          value=classroom_id.value,
                                          index_name='Classroom-Index')
        return [Work.from_dict(item) for item in item_list]
