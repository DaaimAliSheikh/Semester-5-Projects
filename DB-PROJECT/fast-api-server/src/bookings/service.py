from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Booking, Payment
from uuid import UUID, uuid4
from src.bookings.schemas import CreateBookingWithPaymentModel, UpdateBookingWithPaymentModel


class BookingService:
    async def get_all_bookings(self, session: AsyncSession):
        query = select(Booking)
        result = await session.exec(query)
        bookings = result.all()
        return bookings

    async def get_booking(self, booking_id: UUID, session: AsyncSession):
        query = select(Booking).where(Booking.booking_id == booking_id)
        result = await session.exec(query)
        booking = result.first()
        return booking if booking else None

    async def create_booking_with_payment(self, booking_and_payment_data: CreateBookingWithPaymentModel, session: AsyncSession):
        # Create the Booking object
        new_booking = Booking(
            **booking_and_payment_data.booking.model_dump()
        )

        # Create the Payment object and associate it with the Booking
        new_payment = Payment(
            **booking_and_payment_data.payment.model_dump(),
            booking=new_booking  # Link the payment to the booking
        )

        # Add both objects to the session
        session.add(new_booking)
        session.add(new_payment)

        # Commit the transaction
        await session.commit()

        await session.refresh(new_booking)

        return new_booking

    async def delete_booking(self, booking_id: UUID, session: AsyncSession):
        query = select(Booking).where(Booking.booking_id == booking_id)
        results = await session.exec(query)
        booking = results.first()
        if not booking:
            return None

        await session.delete(booking)
        await session.commit()
        return booking

    # async def update_booking_and_payment(self, booking_and_payment_data: UpdateBookingWithPaymentModel, session: AsyncSession):
    #     query = select(Booking).where(Booking.booking_id == booking_id)
    #     results = await session.exec(query)
    #     booking = results.first()
    #     return booking
