from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class DishCreate(DishBase):
    pass


class DishInDb(DishBase):
    restaurant_id: int


class DishUpdate(DishBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class DishOut(DishBase):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True
