import json

from sqlalchemy import inspect


def as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def as_json_dumps(obj):
    obj_dict = as_dict(obj)

    return json.dumps(obj_dict, default=str)
