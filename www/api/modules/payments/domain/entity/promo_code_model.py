from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin
)


class PromoCodeModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'promo_codes'

    id: Mapped[str] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(36), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Float, nullable=False)
    discount_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)
