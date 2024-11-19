from pydantic import BaseModel
import uuid
from src.db.models import CateringMenuItem

# Dish Model Schema


class DishModel(BaseModel):
    dish_id: uuid.UUID
    dish_name: str
    dish_description: str
    dish_cost_per_serving: int

# Catering Model Schema


class CateringModel(BaseModel):
    catering_id: uuid.UUID
    catering_name: str
    catering_description: str
    catering_image: str | None = None
    catering_menu_items: list[CateringMenuItem]
# Create Catering Schema


class CreateCateringModel(BaseModel):
    catering_name: str
    catering_description: str
    catering_image: str | None = None

# Create Dish Schema


class CreateDishModel(BaseModel):
    dish_name: str
    dish_description: str
    dish_cost_per_serving: int
