from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: str

    class Config:
        orm_mode = True


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None


class RestaurantOut(RestaurantBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
