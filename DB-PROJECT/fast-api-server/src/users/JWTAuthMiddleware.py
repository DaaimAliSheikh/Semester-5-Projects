from fastapi import Depends, HTTPException, status, Cookie
import jwt

class Config:
    JWT_SECRET = "your_secret_key"
    JWT_ALGORITHM = "HS256"

def JWTAuthMiddleware(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing",
        )

    try:
        # Decode and verify the JWT token
        payload = jwt.decode(access_token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return payload  # Return user_id data from token
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )