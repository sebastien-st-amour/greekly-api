import decimal
import enum
from flask import json

class GreeklyJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        if isinstance(obj, enum.Enum):
            # Convert enums instances to their values
            return obj.value
        return super(GreeklyJSONEncoder, self).default(obj)