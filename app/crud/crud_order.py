from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_base import CRUDBase
from app.models import Order


class CRUDOrder(CRUDBase):

    async def get_by_user(
            self,
            user_id: int,
            session: AsyncSession
    ):
        db_objs = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id
            )
        )
        return db_objs.scalars().all()


    async def update_status(
            self,
            db_obj,
            new_status: str,
            session: AsyncSession
    ):
        db_obj.status = new_status
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


crud_order = CRUDOrder(Order)