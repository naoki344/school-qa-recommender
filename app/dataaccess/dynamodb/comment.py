from logging import Logger
from typing import List

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.dynamodb.sequences import SequensesDatasource
from app.model.comment.comment import WorkComment
from app.model.comment.comment import WorkCommentList
from app.model.work.work import WorkId


class WorkCommentDatasource:
    def __init__(self, client: DynamoDBClient,
                 sequenses_table: SequensesDatasource, logger: Logger) -> None:
        self.client = client
        self.sequenses_table = sequenses_table
        self.logger = logger

    def insert_item(self, item: WorkComment) -> None:
        self.client.insert_item(item.to_dict(), "comment_id")

    def put_item(self, item: WorkComment) -> None:
        self.client.put_item(item.to_dict())

    def fetch_sequense_id(self) -> int:
        name = f"Dynamodb#{self.client.table.table_name}"
        _id = self.sequenses_table.fetch_sequense_id(name)
        return _id

    def find_by_work_id(self, work_id: WorkId) -> List[WorkComment]:
        item_list = self.client.get_items(name='work_id',
                                          value=work_id.value,
                                          index_name='WorkId-Index')
        return WorkCommentList.from_list(item_list)
