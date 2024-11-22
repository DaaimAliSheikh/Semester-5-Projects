from pydantic import BaseModel
import uuid
from datetime import datetime
from src.db.models import Booking


class PromoModel(BaseModel):
    promo_id: uuid.UUID
    promo_name: str
    promo_expiry: datetime
    promo_discount: float


class CreatePromoModel(BaseModel):
    promo_name: str
    # expects new dateObject.toISOString() string from JS frontend as ISO 8601
    promo_expiry: datetime
    promo_discount: float
