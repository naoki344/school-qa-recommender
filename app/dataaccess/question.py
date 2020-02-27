from app.dataaccess.aws.dynamodb import DynamoDBClient


class QuestionDynamoDatasource:
    table_name = "qa-Question"

    def __init__(self, client: DynamoDBClient) -> None:
        self.client = client
        if client.partial_table_name != self.table_name:
            raise SystemError("Is not equal table_name and partial_table_name")

    def insert(self, item: dict) -> None:
        self.client.put_item(item)
