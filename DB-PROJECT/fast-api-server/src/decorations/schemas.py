from pydantic import BaseModel
from src.db.models import Booking
import uuid


class DecorationModel(BaseModel):
    decoration_id: uuid.UUID
    decoration_name: str
    decoration_price: int
    decoration_description: str
    decoration_image: str | None
    bookings: list[Booking]


class CreateDecorationModel(BaseModel):
    decoration_name: str
    decoration_price: int
    decoration_description: str
    decoration_image: str | None
