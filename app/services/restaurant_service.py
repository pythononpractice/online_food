from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantBase
from app.crud.crud_restaurant import crud_restaurant


class RestaurantService:
    def __init__(self, crud):
        self.crud = crud

    async def create_restaurant(
        self,
        obj_in: RestaurantCreate,
        session: AsyncSession
    ) -> RestaurantBase:
        return await self.crud.create(session=session, obj_in=obj_in)

    async def update_restaurant(
        self,
        restaurant_id: int,
        obj_in: RestaurantUpdate,
        session: AsyncSession
    ) -> RestaurantBase:
        restaurant = await self.crud.get(obj_id=restaurant_id, session=session)
        return await self.crud.update(db_obj=restaurant, obj_in=obj_in, session=session)

    async def delete_restaurant(
        self,
        restaurant_id: int,
        session: AsyncSession
    ) -> RestaurantBase:
        restaurant = await self.crud.get(obj_id=restaurant_id, session=session)
        return await self.crud.remove(db_obj=restaurant, session=session)

    async def get_restaurant(
        self,
        restaurant_id: int,
        session: AsyncSession
    ) -> RestaurantBase:
        return await self.crud.get(session=session, obj_id=restaurant_id)

    async def list_restaurants(
        self,
        session: AsyncSession
    ) -> list[RestaurantBase]:
        return await self.crud.get_multi(session)


restaurant_service = RestaurantService(crud_restaurant)
