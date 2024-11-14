from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class UserModel(BaseModel):  # this is the response model
    id: uuid.UUID
    username: str
    email: str
    password: str = Field(exclude=True)
    profile_picture_url:  str | None = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str
    profile_picture_url:  str | None = None

class LoginUserModel(BaseModel):
    email: str
    password: str


class UpdateUserModel(BaseModel):
    username: str | None = None
    # cannot update email
    password: str | None = None
    profile_picture_url: str | None = None
    is_verified: bool | None = None
