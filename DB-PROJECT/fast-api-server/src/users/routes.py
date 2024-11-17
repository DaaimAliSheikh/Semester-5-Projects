from fastapi import APIRouter, Depends, HTTPException, status,Response
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.service import UserService
from src.users.schemas import CreateUserModel, UserModel
from uuid import UUID
from .utils import verify_password,create_access_token
from src.config import Config
from .JWTAuthMiddleware import JWTAuthMiddleware

user_router = APIRouter(prefix="/users")
user_service = UserService()


# @user_router.get("/", response_model=list[UserModel], status_code=status.HTTP_200_OK)
# async def get_all_users(session: AsyncSession = Depends(get_session)):
#     return await user_service.get_all_users(session)




@user_router.get("/", response_model=str, status_code=status.HTTP_200_OK)
async def get_user_id(user: dict = Depends(JWTAuthMiddleware), session: AsyncSession = Depends(get_session)):
    return user









# response_model TRUNCATES USER TO ONLY THE PROPERTIES IN UserModel
@user_router.get("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user(user_id, session)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@user_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(response: Response,user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):

    if not await user_service.get_user_by_email(user_data.email, session):
        user = await user_service.create_user(user_data, session)
        if user:
            response.set_cookie(
                key="access_token",
                value=f"Bearer {create_access_token(user.user_id)}",
                httponly=True,  # Secure the cookie from JavaScript access
                max_age=int(Config.ACCESS_TOKEN_EXPIRY),
                samesite="lax"
            )
            return user
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User could not be created")
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user_data.email} already exists")

@user_router.post("/login", response_model=UserModel, status_code=status.HTTP_200_OK)
async def login_user(response: Response,user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(user_data.email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # Set token as a cookie
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {create_access_token(user.user_id)}",
        httponly=True,  # Secure the cookie from JavaScript access
        max_age=int(Config.ACCESS_TOKEN_EXPIRY),
        samesite="lax"
    )
    return user



@user_router.post("/admin/login", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def login_admin(user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):
    user = await user_service.create_user(user_data, session)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


# @user_router.patch("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
# async def update_user(user_id: UUID, user_data: UpdateUserModel, session: AsyncSession = Depends(get_session)):

#     user = await user_service.update_user(user_id, user_data, session)

#     if user:
#         return user  # updated user
#     raise HTTPException(status_code=404, detail="User not found")


# @user_router.delete("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
# async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
#     user = await user_service.delete_user(user_id, session)
#     if user:
#         return user  # deleted user
#     raise HTTPException(status_code=404, detail="User not found")
