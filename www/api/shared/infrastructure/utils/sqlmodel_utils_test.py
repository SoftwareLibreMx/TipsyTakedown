import pytest
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from .sqlmodel_utils import as_json_dumps, BaseModel, TrackTimeMixin, SoftDeleteMixin


class MockModel(declarative_base()):
    __tablename__ = 'mock_model'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column()
    name: Mapped[str] = mapped_column()


mock_uuid = uuid4()


@pytest.mark.unit
def test_as_json_dumps():
    obj = MockModel(id=1, uuid=mock_uuid, name='John Doe')
    expected = f'{{"id": 1, "uuid": "{mock_uuid}", "name": "John Doe"}}'
    assert as_json_dumps(obj) == expected


@pytest.mark.unit
def test_soft_delete():
    class MockModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
        __tablename__ = 'mock_model'

        id: Mapped[int] = mapped_column(primary_key=True)
        uuid: Mapped[UUID] = mapped_column()
        name: Mapped[str] = mapped_column()

    obj = MockModel(id=1, uuid=mock_uuid, name='John Doe')
    obj.soft_delete()
    assert obj.deleted_at is not None
