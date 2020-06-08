import decimal
from datetime import date as Date
from datetime import datetime as DateTime
from json import JSONEncoder
from typing import Any


class CustomJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, DateTime):
            return o.isoformat()
        if isinstance(o, Date):
            return o.isoformat()
        return super(CustomJSONEncoder, self).default(o)
