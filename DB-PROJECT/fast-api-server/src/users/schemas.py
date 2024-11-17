from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class UserModel(BaseModel):  # this is the response model
    user_id: str  # str instead of uuid type because uuid is not serializable
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    profile_picture_url:  str | None = None
    is_admin: bool


class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str
    profile_picture_url:  str | None = None


class LoginUserModel(BaseModel):
    email: str
    password: str
