from sqlalchemy import select
from app.crud.crud_base import CRUDBase
from app.models import Restaurant
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDRestaurant(CRUDBase):
    async def get_by_name(
            self,
            name: str,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.name == name
            )
        )
        return db_obj.scalar()


crud_restaurant = CRUDRestaurant(Restaurant)