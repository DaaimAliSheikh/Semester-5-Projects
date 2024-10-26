from pydantic import BaseModel
from datetime import datetime
import uuid


class BookModel(BaseModel):
    ISBN_NO: uuid.UUID
    Title: str
    Author: str
    created_at: datetime
    updated_at: datetime


class CreateBookModel(BaseModel):
    Title: str
    Author: str
