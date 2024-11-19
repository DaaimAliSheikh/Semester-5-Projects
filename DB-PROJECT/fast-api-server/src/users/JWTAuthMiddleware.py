from fastapi import Depends, HTTPException, status, Cookie
import jwt

from src.config import Config
from src.db.main import get_session
from src.users.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession

user_service = UserService()


async def JWTAuthMiddleware(access_token: str = Cookie(None),session: AsyncSession = Depends(get_session)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing",
        )

    try:
        # Decode and verify the JWT token
        payload = jwt.decode(access_token, Config.JWT_SECRET,algorithms=[Config.JWT_ALGORITHM]) #necessary to pass algo here
        return await user_service.get_user(payload.get("user_id"), session)
        
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
        )