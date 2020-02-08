from logging import Logger

from app.dataaccess.aws.dynamodb import DynamoDBClient
from app.dataaccess.aws.dynamodb import ReturnType


class SequensesDatasource:
    def __init__(self, client: DynamoDBClient,
                 logger: Logger) -> None:
        self.client = client
        self.logger = logger

    def fetch_sequense_id(self, name: str) -> int:
        keys = {"name": name}
        updates = {"id": {"Value": 1, "Action": "ADD"}}
        data = self.client.update_item(
            keys, updates, ReturnType.UPDATED_NEW)
        return int(data["id"])
