import json
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from app.utils.encoder import CustomJSONEncoder


class APIGatewayResponse:
    @staticmethod
    def to_response(data: Union[Dict[str, Any], List[Any]]):
        return {
            "statusCode": 200,
            "body": json.dumps(data, cls=CustomJSONEncoder),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }


class APIGatewayErrorResponse:
    @staticmethod
    def to_response(error: Exception):
        return {
            "statusCode":
            500,
            "body":
            json.dumps(
                {
                    "type": error.__class__.__name__,
                    "message": str(error)
                },
                cls=CustomJSONEncoder),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
