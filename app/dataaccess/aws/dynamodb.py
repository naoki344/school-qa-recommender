import json
from datetime import date as Date
from datetime import datetime as DateTime
from enum import Enum
from enum import auto
from logging import Logger
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

import boto3

from app.utils.encoder import CustomJSONEncoder


class TableResource:
    @staticmethod
    def create(table_name: str):
        return boto3.resource('dynamodb').Table(table_name)


class ReturnType(Enum):
    NONE = auto()
    ALL_OLD = auto()
    ALL_NEW = auto()
    UPDATED_OLD = auto()
    UPDATED_NEW = auto()


class DynamoDBClient:
    def __init__(self, table: TableResource, logger: Logger) -> None:
        self.table = table
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

    def get_items(self,
                  name: str,
                  value: str,
                  index_name: Optional[str] = None) -> List[dict]:
        names = {'#id': name}
        values = {':value': value}
        expression = '#id = :value'
        result = self.__query(index_name=index_name,
                              names=names,
                              values=values,
                              expression=expression)
        yield from result['Items']

        while 'LastEvaluatedKey' in result:
            result = self.__query(
                index_name=index_name,
                names=names,
                values=values,
                expression=expression,
                exclusive_start_key=result['LastEvaluatedKey'])
            yield from result['Items']

    def query(
        self,
        index_name: str,
        names: Dict[str, Any],
        values: Dict[str, Any],
        expression: str,
        limit: Optional[int] = 100,
        exclusive_start_key: Optional[str] = None
    ) -> Union[List[dict], str]:
        self.logger.debug(
            'Get an item_list from {} table.[IndexName={}]'.format(
                self.table.table_name, index_name))
        result = self.__query(index_name=index_name,
                              names=names,
                              values=values,
                              expression=expression,
                              exclusive_start_key=exclusive_start_key)
        if 'Items' in result:
            return result['Items'], result.get('LastEvaluatedKey')
        return [], None

    def put_item(self, data: dict) -> None:
        encoded_data = DynamoDBClient.dynamo_type_encode(data)
        self.logger.debug('Put an item to {} table.[item={}]'.format(
            self.table.table_name,
            json.dumps(encoded_data, cls=CustomJSONEncoder)))
        self.table.put_item(Item=encoded_data)

    def insert_item(self,
                    data: dict,
                    hash_key: str,
                    sort_key: Optional[str] = None) -> None:
        condition = f"attribute_not_exists({hash_key})"
        if sort_key:
            condition += f" AND attribute_not_exists({sort_key})"
        encoded_data = DynamoDBClient.dynamo_type_encode(data)
        self.table.put_item(Item=encoded_data, ConditionExpression=condition)

    def put_item_condition(self, data: dict, condition: str,
                           attribute_values: dict, attribute_names: dict):
        encoded_data = DynamoDBClient.dynamo_type_encode(data)
        self.table.put_item(Item=encoded_data,
                            ConditionExpression=condition,
                            ExpressionAttributeNames=attribute_names,
                            ExpressionAttributeValues=attribute_values)

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

    def update_item(
            self,
            keys: dict,
            updates: dict,
            return_type: Optional[ReturnType] = ReturnType.ALL_NEW,
    ) -> dict:
        self.logger.debug('Update an item to {} table.[Key={}]'.format(
            self.table.table_name, json.dumps(keys, cls=CustomJSONEncoder)))
        data = self.table.update_item(Key=keys,
                                      AttributeUpdates=updates,
                                      ReturnValues=return_type.name)
        return data["Attributes"]

    def __query(self,
                names: Dict[str, Any],
                values: Dict[str, Any],
                expression: str,
                limit: Optional[int] = 100,
                index_name: Optional[str] = None,
                exclusive_start_key: Optional[str] = None) -> dict:
        args = {
            "ExpressionAttributeNames": names,
            "ExpressionAttributeValues": values,
            "KeyConditionExpression": expression,
            "Limit": limit
        }
        if index_name is not None:
            args = {**args, "IndexName": index_name}
        if exclusive_start_key is not None:
            args = {**args, "ExclusiveStartKey": exclusive_start_key}
        return self.table.query(**args)
