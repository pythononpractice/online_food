import base64
import os
from uuid import uuid4

from sqlalchemy import select

from app.core.config import settings
from app.crud.crud_base import CRUDBase
from app.models import Dish
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDDish(CRUDBase):

    async def get_by_restaurant_id(
            self,
            restaurant_id: int,
            session: AsyncSession
    ):
        db_objs = await session.execute(
            select(self.model).where(
                self.model.restaurant_id == restaurant_id
            )
        )
        return db_objs.scalars().all()

crud_dish = CRUDDish(Dish)