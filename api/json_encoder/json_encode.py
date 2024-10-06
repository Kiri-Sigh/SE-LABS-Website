import json
from datetime import datetime
from uuid import UUID

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()
        return super().default(obj)

def prepare_json(data):
    return json.loads(json.dumps(data, cls=CustomJSONEncoder))