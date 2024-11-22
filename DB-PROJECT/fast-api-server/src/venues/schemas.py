from pydantic import BaseModel
import uuid
from datetime import datetime


class VenueReviewModel(BaseModel):
    venue_review_id: uuid.UUID
    venue_id: uuid.UUID
    user_id: uuid.UUID
    venue_review_text: str
    venue_review_created_at: datetime


class CreateVenueReviewModel(BaseModel):
    review_text: str


class VenueModel(BaseModel):
    venue_id: uuid.UUID
    venue_name: str
    venue_address: str
    venue_capacity: int
    venue_price_per_day: int
    venue_rating: float
    venue_image: str | None
    venue_reviews: list[VenueReviewModel]


class CreateVenueModel(BaseModel):
    venue_name: str
    venue_address: str
    venue_capacity: int
    venue_price_per_day: int
    venue_image: str | None
