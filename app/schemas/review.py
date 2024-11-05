from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    rating: Optional[int] = None
    comment: Optional[str] = None


class ReviewOut(ReviewBase):
    id: int
    user_id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        orm_mode = True
