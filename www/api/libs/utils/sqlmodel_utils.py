import json
from dataclasses import asdict

from sqlalchemy import inspect, Column, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime


def as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }


def as_json_dumps(obj):
    obj_dict = as_dict(obj)

    return json.dumps(obj_dict, default=str)


def dataclass_to_json_dumps(obj):
    return json.dumps(asdict(obj), default=str)


BaseModel = declarative_base()


class TrackTimeMixin:
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now)


class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()
