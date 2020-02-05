import json
from datetime import date as Date
from datetime import datetime as DateTime
from logging import Logger
from typing import Generator
from typing import Optional

import boto3

from app.utils.encoder import CustomJSONEncoder


class TableResource:
    @staticmethod
    def create(table_name: str):
        return boto3.resource('dynamodb').Table(table_name)


class DynamoDBClient:
    def __init__(
            self, table_resource: TableResource,
            logger: Logger) -> None:
        self.table = table_resource
        self.logger = logger

    def scan(self) -> Generator[dict, None, None]:
        self.logger.debug('Scan items from {} table.'.format(
            self.table.table_name))
        result = self.table.scan()
        yield from result['Items']

        while 'LastEvaluatedKey' in result:
            result = self.table.scan(
                ExclusiveStartKey=result['LastEvaluatedKey'])
            yield from result['Items']

    def get_item(self, key: dict) -> Optional[dict]:
        self.logger.debug('Get an item from {} table.[Key={}]'.format(
            self.table.table_name, key))
        result = self.table.get_item(Key=key)
        if 'Item' in result:
            return result['Item']
        else:
            return None

    def put_item(self, data: dict) -> None:
        encoded_data = DynamoDBClient.dynamo_type_encode(data)
        self.logger.debug('Put an item to {} table.[item={}]'.format(
            self.table.table_name,
            json.dumps(encoded_data, cls=CustomJSONEncoder)))
        self.table.put_item(Item=encoded_data)

    def put_item_idempotency(self, data: dict, condition: str):
        encoded_data = DynamoDBClient.dynamo_type_encode(data)
        self.table.put_item(Item=encoded_data, ConditionExpression=condition)

    def delete_item(self, key: dict) -> None:
        self.logger.debug('Delete an item from {} table.[Key={}]'.format(
            self.table.table_name, key))
        self.table.delete_item(Key=key)

    @staticmethod
    def dynamo_type_encode(obj):
        if isinstance(obj, dict):
            new_dict: dict = dict()
            for key, value in obj.items():
                new_value = DynamoDBClient.dynamo_type_encode(value)
                if new_value is None or new_value == "":
                    continue
                new_dict[key] = new_value
            return new_dict
        elif isinstance(obj, list):
            return [DynamoDBClient.dynamo_type_encode(elem) for elem in obj]
        elif isinstance(obj, DateTime):
            return obj.isoformat()
        elif isinstance(obj, Date):
            return obj.isoformat()
        else:
            return obj
