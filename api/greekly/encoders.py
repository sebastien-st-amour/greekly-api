from flask import json
import decimal
import enum

class GreeklyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, enum.Enum):
            return obj.value
        return super(GreeklyEncoder, self).default(obj)