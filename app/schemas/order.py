from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OrderBase(BaseModel):
    status: Optional[str] = None


class OrderCreate(BaseModel):
    dish_id: int


class OrderInDb(OrderCreate):
    user_id: int


class OrderUpdate(OrderBase):
    status: Optional[str] = None


class OrderOut(OrderBase):
    id: int
    user_id: int
    dish_id: int
    created_at: datetime

    class Config:
        orm_mode = True
