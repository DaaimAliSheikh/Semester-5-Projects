import venv
from pydantic import BaseModel
from uuid import UUID
from src.db.models import CarReservation, Payment, Promo, User, Catering, Decoration, Venue, Promo
from datetime import datetime
from src.db.models import BookingStatus


class BookingModel(BaseModel):
    booking_id: UUID
    booking_date: datetime
    booking_event_date: datetime
    booking_guest_count: int
    booking_total_cost: int
    booking_discount: float
    booking_status: BookingStatus
    user: User
    venue: Venue
    payment: Payment
    catering: Catering
    Decoration: Decoration
    car_reservations: list[CarReservation]
    promo: Promo


class CreateBookingModel(BaseModel):
    booking_event_date: datetime
    booking_guest_count: int
    booking_total_cost: int
    booking_discount: float
    booking_status: BookingStatus = BookingStatus.pending
    user_id: UUID
    venue_id: UUID
    # payment will be created manually
    catering_id: UUID | None
    decoration_id: UUID | None
    promo_id: UUID | None
