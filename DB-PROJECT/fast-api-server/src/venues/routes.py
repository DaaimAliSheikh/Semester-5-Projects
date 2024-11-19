from fastapi import APIRouter, Depends, HTTPException, status, Response
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.venues.service import VenueService
from src.users.schemas import CreateUserModel, UserModel, LoginUserModel
from uuid import UUID
from src.config import Config

user_router = APIRouter(prefix="/venues")
user_service = VenueService()


# response_model TRUNCATES USER TO ONLY THE PROPERTIES IN UserModel


# response_model TRUNCATES USER TO ONLY THE PROPERTIES IN UserModel
# @user_router.get("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
# async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
#     user = await user_service.get_user(user_id, session)
#     if user:
#         return user
#     raise HTTPException(status_code=404, detail="User not found")

# user_id: str = Depends(JWTAuthMiddleware)


@user_router.post("/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(response: Response, user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):


    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User with email {user_data.email} already exists")


@user_router.post("/", response_model=UserModel, status_code=status.HTTP_200_OK)
async def login_user(response: Response, user_data: LoginUserModel, session: AsyncSession = Depends(get_session)):
    

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User does not exist")







# @user_router.delete("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
# async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
#     user = await user_service.delete_user(user_id, session)
#     if user:
#         return user  # deleted user
#     raise HTTPException(status_code=404, detail="User not found")
