from pydantic import BaseModel
from uuid import UUID
from src.db.models import CarReservation


class CarModel(BaseModel):
    car_id: UUID
    car_make: str
    car_model: str
    car_year: int
    car_rental_price: int
    car_image: str | None
    car_quantity: int
    # Assuming you have the CarReservation model
    car_reservations: list["CarReservation"]


class CreateCarModel(BaseModel):
    car_make: str
    car_model: str
    car_year: int
    car_rental_price: int
    car_image: str | None
    car_quantity: int


class CarReservationModel(BaseModel):
    car_reservation_id: UUID
    car_id: UUID
    booking_id: UUID
