from fastapi import APIRouter, Depends, HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.service import UserService
from src.users.schemas import UpdateUserModel, CreateUserModel, UserModel
from uuid import UUID

user_router = APIRouter(prefix="/users")
user_service = UserService()


@user_router.get("/", response_model=list[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    return await user_service.get_all_users(session)


@user_router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user(user_id, session)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@user_router.post("/", response_model=UserModel)
async def create_user(user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):
    user = await user_service.create_user(user_data, session)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@user_router.patch("/{user_id}", response_model=UserModel)
async def update_user(user_id: UUID, user_data: UpdateUserModel, session: AsyncSession = Depends(get_session)):

    user = await user_service.update_user(user_id, user_data, session)

    if user:
        return user  # updated user
    raise HTTPException(status_code=404, detail="User not found")


@user_router.delete("/{user_id}", response_model=UserModel)
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await user_service.delete_user(user_id, session)
    if user:
        return user  # deleted user
    raise HTTPException(status_code=404, detail="User not found")
