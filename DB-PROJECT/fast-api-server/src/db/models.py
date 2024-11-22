from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Relationship  # type: ignore
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid
from sqlalchemy import Enum as PgEnum, ForeignKey, CheckConstraint, UniqueConstraint


# Enums


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    declined = "declined"


class PaymentMethod(str, Enum):
    debit_card = "debit_card"
    credit_card = "credit_card"
    easypaisa = "easypaisa"
    jazzcash = "jazzcash"
    other = "other"


class DishType(str, Enum):
    starter = "starter"
    main = "main"
    dessert = "dessert"


# Tables

class User(SQLModel, table=True):
    __tablename__: str = "user"  # type: ignore

    user_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False,
        unique=False
    ))
    email: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False,
        unique=True
    ))
    password_hash: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False
    ))
    is_admin: bool = Field(sa_column=Column(
        pg.BOOLEAN,
        nullable=False,
        default=False
    ))

    # one-many relationship with user_contact
    user_contacts: list["UserContact"] = Relationship(back_populates="user", sa_relationship_kwargs={
                                                      "cascade": "all, delete-orphan", "lazy": "selectin"})
    # one-many relationship with venue_review
    venue_reviews: list["VenueReview"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})

    # one-many relationship with booking
    bookings: list["Booking"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})
    # "cascade": "all, delete-orphan" is to delete/modify/add child entities when parent entity's 'child referencing property' is deleted/modified/add
    # eg: catering.catering_menu_items[0].dish = Dish(...)
    # eg: catering.catering_menu_items[0].pop(0)


class UserContact(SQLModel, table=True):
    __tablename__: str = "user_contact"
    # user_id and user_contact_number are composite primary keys

    user_contact_number: str = Field(
        sa_column=Column(pg.VARCHAR(15), primary_key=True, nullable=False)
    )
    # one-many relationship with user
    user_id: uuid.UUID = Field(sa_column=Column(pg.UUID, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False, primary_key=True))
    # ondelete="CASCADE", if user gets deleted, then user_contact also gets deleted
    user: "User" = Relationship(back_populates="user_contacts")


class Venue(SQLModel, table=True):
    __tablename__: str = "venue"

    venue_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    venue_name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    venue_address: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False))

    # check constraint for venue_capacity
    venue_capacity: int = Field(sa_column=Column(pg.INTEGER, CheckConstraint(
        "venue_capacity >= 0"), nullable=False))

    venue_price_per_day: int = Field(
        sa_column=Column(pg.INTEGER, nullable=False))

    # check constraint for venue_rating
    venue_rating: int = Field(sa_column=Column(pg.FLOAT, CheckConstraint(
        "venue_rating >= 1"), nullable=False, default=0))
    venue_image: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))

    # one-many relationship with venue_review
    venue_reviews: list["VenueReview"] = Relationship(
        back_populates="venue", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})
    # in list["Type"], Type should be class name not table name(VenueReview, not venue_review)

    # one-many relationship with booking
    bookings: list["Booking"] = Relationship(back_populates="venue")


class VenueReview(SQLModel, table=True):
    __tablename__: str = "venue_review"

    venue_review_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    # review text length can only be of 1000 characters
    venue_review_text: str = Field(
        sa_column=Column(pg.VARCHAR(1000), nullable=False))
    venue_review_created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )

    # one-many relationship with venue
    venue_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey(
            "venue.venue_id", ondelete="CASCADE"), nullable=False)
    )
    venue: "Venue" = Relationship(back_populates="venue_reviews")
    # one-many relationship with users
    user_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey(
            "user.user_id", ondelete="CASCADE"), nullable=False)
    )
    user: "User" = Relationship(back_populates="venue_reviews")


class Payment(SQLModel, table=True):
    __tablename__: str = "payment"

    payment_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    # check constraint for payment_amount
    payment_amount: int = Field(sa_column=Column(pg.INTEGER,  CheckConstraint(
        "payment_amount >= 0"), nullable=False))
    payment_date: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )

    payment_method: PaymentMethod = Field(
        sa_column=Column(PgEnum(PaymentMethod), nullable=False,
                         default=PaymentMethod.debit_card)
    )
    # one-one relationship with booking

    booking_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey(
            "booking.booking_id", ondelete="CASCADE"), nullable=False)
    )

    booking: "Booking" = Relationship(back_populates="payment")


class Decoration(SQLModel, table=True):
    __tablename__: str = "decoration"

    decoration_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    decoration_name: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False))
    # check constraint for decoration_price
    decoration_price: int = Field(sa_column=Column(pg.INTEGER,  CheckConstraint(
        "decoration_price >= 0"), nullable=False))
    decoration_description: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False))
    decoration_image: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=True))

    # one-many relationship with booking
    bookings: list["Booking"] = Relationship(
        back_populates="decoration", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})


class Car(SQLModel, table=True):
    __tablename__: str = "car"

    car_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    car_make: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    car_model: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    # check constraint for car_year
    car_year: int = Field(sa_column=Column(pg.INTEGER,  CheckConstraint(
        f"car_year BETWEEN 1886 AND {datetime.now().year + 1}",
        name="check_car_year_valid"
    ), nullable=False))
    # check constraint for car_rental_price
    car_rental_price: int = Field(sa_column=Column(pg.INTEGER, CheckConstraint(
        "car_rental_price >= 0"), nullable=False))
    car_image: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    # check constraint for car_quantity
    car_quantity: int = Field(sa_column=Column(pg.INTEGER, CheckConstraint(
        "car_quantity >= 0"), nullable=False))

    # one-many relationship with car_reservation
    car_reservations: list["CarReservation"] = Relationship(
        back_populates="car", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})

# Car reservation table = many to many relation b/w car and booking


class CarReservation(SQLModel, table=True):
    __tablename__: str = "car_reservation"

    car_reservation_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    # one-many relationship with car
    car_id: uuid.UUID = Field(sa_column=Column(
        pg.UUID, ForeignKey("car.car_id", ondelete="CASCADE"), nullable=False))
    car: "Car" = Relationship(back_populates="car_reservations")
    # one-many relationship with booking
    booking_id: uuid.UUID = Field(sa_column=Column(
        pg.UUID, ForeignKey("booking.booking_id", ondelete="CASCADE"), nullable=False))
    booking: "Booking" = Relationship(back_populates="car_reservations")


class Catering(SQLModel, table=True):
    __tablename__: str = "catering"

    catering_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    catering_description: str = Field(
        sa_column=Column(pg.VARCHAR(1000), nullable=False))
    catering_name: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False))
    catering_image: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=True))

    # one-many relationship with booking
    bookings: list["Booking"] = Relationship(back_populates="catering", sa_relationship_kwargs={
                                             "cascade": "all, delete-orphan", "lazy": "selectin"})

    # one-many relationship with CateringMenuItem
    catering_menu_items: list["CateringMenuItem"] = Relationship(
        back_populates="catering", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})


class Dish(SQLModel, table=True):
    __tablename__: str = "dish"

    dish_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    dish_name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    dish_description: str = Field(
        sa_column=Column(pg.VARCHAR(1000), nullable=False))
    dish_type: DishType = Field(
        sa_column=Column(PgEnum(DishType), nullable=False,
                         default=DishType.main)
    )
    dish_image: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    # check constraint for dish_cost_per_serving
    dish_cost_per_serving: int = Field(
        sa_column=Column(pg.INTEGER, CheckConstraint(
            "dish_cost_per_serving >= 0"), nullable=False))

    # one-many relationship with dishes
    catering_menu_items: list["CateringMenuItem"] = Relationship(
        back_populates="dish", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})


# Catering Menu Item = many to many realtion b/w catering and dish
class CateringMenuItem(SQLModel, table=True):
    __tablename__: str = "catering_menu_item"
    # catering_id and booking_id are composite primary keys
    # one-many relationship with car
    catering_id: uuid.UUID = Field(sa_column=Column(pg.UUID, ForeignKey(
        "catering.catering_id"), nullable=False, primary_key=True))
    catering: "Catering" = Relationship(back_populates="catering_menu_items")
    # one-many relationship with booking
    dish_id: uuid.UUID = Field(sa_column=Column(pg.UUID, ForeignKey(
        "dish.dish_id", ondelete="CASCADE"), nullable=False, primary_key=True))
    dish: "Dish" = Relationship(back_populates="catering_menu_items")


class Promo(SQLModel, table=True):
    __tablename__: str = "promo"

    promo_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    promo_name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    promo_expiry: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False))

    # check constraint for promo_discount
    promo_discount: float = Field(sa_column=Column(pg.FLOAT, CheckConstraint(
        "promo_discount > 0"), nullable=False))

    # one-many relationship with booking
    bookings: list["Booking"] = Relationship(back_populates="promo", sa_relationship_kwargs={
                                             "cascade": "all, delete-orphan", "lazy": "selectin"})


class Booking(SQLModel, table=True):
    __tablename__: str = "booking"

    booking_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    booking_date: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    booking_event_date: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False))
    # check constraint for booking_guest_count, there must be atleast 1 guest
    booking_guest_count: int = Field(
        sa_column=Column(pg.INTEGER, CheckConstraint(
            "booking_guest_count > 0"), nullable=False))
    # check constraint for booking_total_cost
    booking_total_cost: int = Field(
        sa_column=Column(pg.INTEGER, CheckConstraint(
            "booking_total_cost >= 0"), nullable=False))

    # check constraint for booking_discount
    booking_discount: float = Field(sa_column=Column(pg.FLOAT, CheckConstraint(
        "booking_discount > 0"), nullable=True))
    booking_status: BookingStatus = Field(
        sa_column=Column(PgEnum(BookingStatus), nullable=False,
                         default=BookingStatus.pending)
    )

    # one-many relationship with user(COMPULSORY)
    user_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey(
            "user.user_id", ondelete="CASCADE"), nullable=False)
    )
    user: "User" = Relationship(back_populates="bookings")

    # one-one relationship with payment(COMPULSORY)
    payment: "Payment" = Relationship(back_populates="booking", sa_relationship_kwargs={
        "cascade": "all, delete-orphan"})

    # one-many relationship with venue(COMPULSORY)
    venue_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("venue.venue_id"), nullable=False)
    )
    venue: "Venue" = Relationship(back_populates="bookings")

    # one-many relationship with catering(OPTIONAL)
    catering_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey(
            "catering.catering_id", ondelete="CASCADE"), nullable=True)
    )
    catering: "Catering" = Relationship(back_populates="bookings")

    # one-many relationship with Decoration(OPTIONAL)
    decoration_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey(
            "decoration.decoration_id", ondelete="CASCADE"), nullable=True)
    )
    decoration: "Decoration" = Relationship(back_populates="bookings")

    # one-many relationship with car_reservation(OPTIONAL)
    car_reservations: list["CarReservation"] = Relationship(
        back_populates="booking", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})

    # one-many relationship with promo(OPTIONAL)
    promo_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey(
            "promo.promo_id", ondelete="CASCADE"), nullable=True)
    )
    promo: "Promo" = Relationship(back_populates="bookings")
    # unique constraint for venue and booking_event_date
    __table_args__ = (
        UniqueConstraint("venue_id", "booking_event_date",
                         name="unique_car_make_model"),
    )
