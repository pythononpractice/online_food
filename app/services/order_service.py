from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import OrderCreate, OrderInDb
from app.crud import crud_order
from app.models import Order


class OrderService:
    def __init__(self, crud):
        self.crud = crud

    async def create_order(
        self,
        user_id: int,
        obj_in: OrderCreate,
        session: AsyncSession
    ) -> Order:
        obj_in = OrderInDb(**obj_in.dict(), user_id=user_id)
        return await self.crud.create(obj_in=obj_in, session=session)

    async def update_order_status(
        self,
        order_id: int,
        status: str,
        session: AsyncSession
    ) -> Order:
        order = await self.crud.get(order_id, session=session)
        return await self.crud.update_status(db_obj=order, new_status=status, session=session)

    async def cancel_order(
        self,
        order_id: int,
        session: AsyncSession
    ) -> Order:
        order = await self.crud.get(obj_id=order_id, session=session)
        return await self.crud.update_status(db_obj=order, new_status='canceled', session=session)

    async def get_order(
        self,
        order_id: int,
        session: AsyncSession
    ) -> Order:
        return await self.crud.get(order_id, session=session)

    async def list_orders(
        self,
        user_id: int,
        session: AsyncSession
    ) -> list[Order]:
        return await self.crud.get_by_user(user_id, session=session)


order_service = OrderService(crud_order)
