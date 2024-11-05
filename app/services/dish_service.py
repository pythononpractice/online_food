from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.dish import DishCreate, DishUpdate, DishInDb
from app.crud.crud_dish import crud_dish
from app.models import Dish


class DishService:
    def __init__(self, crud):
        self.crud = crud

    async def create_dish(
        self,
        restaurant_id: int,
        obj_in: DishCreate,
        session: AsyncSession
    ) -> Dish:
        obj_in = DishInDb(**obj_in.dict(), restaurant_id=restaurant_id)
        print(obj_in)
        return await self.crud.create(obj_in=obj_in, session=session)

    async def update_dish(
        self,
        dish_id: int,
        obj_in: DishUpdate,
        session: AsyncSession
    ) -> Dish:
        dish = await self.crud.get(obj_id=dish_id, session=session)
        return await self.crud.update(db_obj=dish, obj_in=obj_in, session=session)

    async def delete_dish(
        self,
        dish_id: int,
        session: AsyncSession
    ) -> Dish:
        dish = await self.crud.get(dish_id, session)
        return await self.crud.remove(dish, session)

    async def get_dish(
        self,
        dish_id: int,
        session: AsyncSession
    ) -> Dish:
        return await self.crud.get(dish_id, session)

    async def list_dishes(
        self,
        restaurant_id: int,
        session: AsyncSession
    ) -> list[Dish]:
        return await self.crud.get_by_restaurant_id(restaurant_id, session)


dish_service = DishService(crud_dish)
