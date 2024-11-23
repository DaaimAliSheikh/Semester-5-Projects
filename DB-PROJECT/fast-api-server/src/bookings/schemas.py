from pydantic import BaseModel, Field
from uuid import UUID
from src.db.models import Booking, CarReservation, Payment, Promo, User, Catering, Decoration, Venue, Promo, PaymentMethod
from datetime import datetime
from src.db.models import BookingStatus


class BookingModel(BaseModel):
    booking_id: UUID
    booking_date: datetime
    booking_event_date: datetime
    booking_guest_count: int
    booking_status: BookingStatus
    user: User
    venue: Venue
    payment: Payment
    catering: Catering
    Decoration: Decoration
    car_reservations: list[CarReservation]
    promo: Promo


class PaymentModel(BaseModel):
    payment_id: UUID
    amount_payed: int = Field(ge=0)
    total_amount: int = Field(ge=0)
    payment_method: PaymentMethod
    discount: float = Field(ge=0)
    booking: Booking


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


class CreatePaymentModel(BaseModel):
    amount_payed: int = Field(ge=0)
    total_amount: int = Field(ge=0)
    payment_method: PaymentMethod
    discount: float = Field(ge=0)


class CreatePaymentAndBookingModel(BaseModel):
    booking: CreateBookingModel
    payment: CreatePaymentModel
