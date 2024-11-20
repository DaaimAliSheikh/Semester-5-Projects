from pydantic import BaseModel
import uuid


class DecorationModel(BaseModel):
    decoration_id: uuid.UUID
    decoration_name: str
    decoration_price: int
    decoration_description: str
    decoration_image: str | None


class CreateDecorationModel(BaseModel):
    decoration_name: str
    decoration_price: int
    decoration_description: str
    decoration_image: str | None
