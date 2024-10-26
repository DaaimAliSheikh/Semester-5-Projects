from datetime import datetime
from pydantic import BaseModel
import uuid


class UserModel(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password_hash: str
    profile_picture_url: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class CreateUserModel(BaseModel):
    username: str
    email: str
    password_hash: str
    profile_picture_url: str


class UpdateUserModel(BaseModel):
    username: str | None = None
    # cannot update email
    password_hash: str | None = None
    profile_picture_url: str | None = None
    is_verified: bool | None = None
