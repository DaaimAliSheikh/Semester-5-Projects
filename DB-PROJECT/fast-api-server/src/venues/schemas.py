from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class VenueReviewModel(BaseModel):
    venue_review_id: uuid.UUID
    venue_id: uuid.UUID
    user_id: uuid.UUID
    venue_review_text: str
    venue_rating: float = Field(ge=1)
    venue_review_created_at: datetime


class CreateVenueReviewModel(BaseModel):
    venue_rating: float = Field(ge=1)
    review_text: str


class VenueModel(BaseModel):
    venue_id: uuid.UUID
    venue_name: str
    venue_address: str
    venue_capacity: int = Field(ge=0)
    venue_price_per_day: int = Field(ge=0)
    venue_image: str | None
    venue_reviews: list[VenueReviewModel]


class CreateVenueModel(BaseModel):
    venue_name: str
    venue_address: str
    venue_capacity: int = Field(ge=0)
    venue_price_per_day: int = Field(ge=0)
    venue_image: str | None
