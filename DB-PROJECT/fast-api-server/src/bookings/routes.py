from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.users.schemas import UserModel
from src.bookings.service import BookingService
from src.cars.schemas import CarModel, CreateCarModel, CarReservationModel
from uuid import UUID
from src.users.JWTAuthMiddleware import JWTAuthMiddleware
from src.config import Config
from src.utils import upload_image

booking_router = APIRouter(prefix="/cars")
booking_service = BookingService()


@booking_router.get("/", response_model=list[CarModel], status_code=status.HTTP_200_OK)
async def get_all_bookings(session: AsyncSession = Depends(get_session)):
    cars = await booking_service.get_all_cars(session)
    return cars


@booking_router.get("/{car_id}", response_model=CarModel, status_code=status.HTTP_200_OK)
async def get_car(car_id: UUID, session: AsyncSession = Depends(get_session)):
    car = await booking_service.get_car(car_id, session)
    if car:
        return car
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Car not found")


@booking_router.post("/", response_model=CarModel, status_code=status.HTTP_201_CREATED)
async def create_car(
    car_make: str = Form(...),
    car_model: str = Form(...),
    car_year: int = Form(...),
    car_rental_price: int = Form(...),
    car_image: UploadFile = File(...),
    car_quantity: int = Form(...),
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )

    # Upload the image and get the file path
    image_name = await upload_image(car_image)
    # Create new car
    car_data = CreateCarModel(
        car_make=car_make,
        car_model=car_model,
        car_year=car_year,
        car_rental_price=car_rental_price,
        car_image=f"{Config.SERVER_BASE_URL}images/{image_name}",
        car_quantity=car_quantity,
    )
    car = await booking_service.create_car(car_data, session)
    return car


@booking_router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: UUID,
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    deleted = await booking_service.delete_car(car_id, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
    return deleted


@booking_router.get("/", response_model=list[CarReservationModel], status_code=status.HTTP_200_OK)
async def get_all_car_reservations(
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    # Fetch all car reservations
    car_reservations = await booking_service.get_all_car_reservations(session)
    return car_reservations


@booking_router.post("/{car_id}/{booking_id}", response_model=CarReservationModel, status_code=status.HTTP_201_CREATED)
async def add_car_reservation(
    car_id: UUID,
    booking_id: UUID,
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    # Add car reservation using path parameters
    car_reservation = await booking_service.add_car_reservation(car_id, booking_id, session)
    if not car_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not available"
        )
    return car_reservation


@booking_router.delete("/{car_reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_car_reservation(
    car_reservation_id: UUID,
    user: UserModel = Depends(JWTAuthMiddleware),
    session: AsyncSession = Depends(get_session),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    # Remove car reservation using car_reservation_id
    deleted_reservation = await booking_service.remove_car_reservation(car_reservation_id, session)
    if not deleted_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car reservation not found"
        )
    return deleted_reservation
