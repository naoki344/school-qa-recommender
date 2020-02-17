import json
from app.utils.encoder import CustomJSONEncoder

from typing import Union
from typing import Dict
from typing import List
from typing import Any


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
