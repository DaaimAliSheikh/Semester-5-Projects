from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from uuid import UUID
from src.caterings.service import CateringService
from src.caterings.schemas import CateringModel, CreateCateringModel, DishModel, CreateDishModel
from src.users.JWTAuthMiddleware import JWTAuthMiddleware
from src.users.schemas import UserModel

catering_router = APIRouter(prefix="/caterings")
catering_service = CateringService()


# Get all caterings along with their dishes
@catering_router.get("/", response_model=list[CateringModel], status_code=status.HTTP_200_OK)
async def get_all_caterings(session: AsyncSession = Depends(get_session)):
    caterings = await catering_service.get_all_caterings(session)
    return caterings


# Add a new catering
@catering_router.post("/", response_model=CateringModel, status_code=status.HTTP_201_CREATED)
async def create_catering(catering_data: CreateCateringModel, user: UserModel = Depends(JWTAuthMiddleware), session: AsyncSession = Depends(get_session)):
    if (not user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    catering = await catering_service.create_catering(catering_data, session)
    return catering


# Delete a catering
@catering_router.delete("/{catering_id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_catering(catering_id: UUID, user: UserModel = Depends(JWTAuthMiddleware), session: AsyncSession = Depends(get_session)):
    if (not user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    deleted_catering = await catering_service.delete_catering(catering_id, session)
    if not deleted_catering:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catering not found")
    return deleted_catering


# Add a new dish
@catering_router.post("/dishes", response_model=DishModel, status_code=status.HTTP_201_CREATED)
async def create_dish(dish_data: CreateDishModel, user: UserModel = Depends(JWTAuthMiddleware), session: AsyncSession = Depends(get_session)):
    if (not user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    dish = await catering_service.create_dish(dish_data, session)
    return dish


# Delete a dish
@catering_router.delete("/dishes/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(dish_id: UUID, user: UserModel = Depends(JWTAuthMiddleware), session: AsyncSession = Depends(get_session)):
    if (not user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    deleted_dish = await catering_service.delete_dish(dish_id, session)
    if not deleted_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    return deleted_dish


# Add a dish to a catering
@catering_router.post("/{catering_id}/dishes/{dish_id}", status_code=status.HTTP_201_CREATED)
async def add_dish_to_catering(catering_id: UUID,  dish_id: UUID, user: UserModel = Depends(JWTAuthMiddleware),  session: AsyncSession = Depends(get_session)):
    if (not user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    catering_menu_item = await catering_service.add_dish_to_catering(catering_id, dish_id, session)
    if not catering_menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catering or Dish not found")
    return catering_menu_item
