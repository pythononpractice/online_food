import base64
import os
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.schemas.dish import DishCreate, DishUpdate, DishInDb
from app.crud.crud_dish import crud_dish
from app.models import Dish


class DishService:
    def __init__(self, crud):
        self.crud = crud

    async def save_image(self, image_base64: str) -> str:
        """Сохранение изображения и возврат пути до него."""
        # Убираем префикс 'data:image/png;base64,' если он присутствует
        if image_base64.startswith("data:image"):
            image_base64 = image_base64.split(",")[1]

        # Проверка и корректировка строки base64
        missing_padding = len(image_base64) % 4
        if missing_padding:
            image_base64 += "=" * (4 - missing_padding)  # Добавление отсутствующего заполнения

        try:
            image_data = base64.b64decode(image_base64)
        except base64.binascii.Error:
            raise HTTPException(status_code=400, detail="Некорректное изображение")
        image_filename = f"{uuid4()}.png"
        image_path = os.path.join(settings.STATIC_IMAGE_PATH, image_filename)

        with open(image_path, "wb") as image_file:
            image_file.write(image_data)

        return image_filename

    async def create_dish(
        self,
        restaurant_id: int,
        obj_in: DishCreate,
        session: AsyncSession
    ) -> Dish:

        if obj_in.image:
            obj_in.image = await self.save_image(obj_in.image)

        obj_in = DishInDb(**obj_in.dict(), restaurant_id=restaurant_id)

        return await self.crud.create(obj_in=obj_in, session=session)

    async def update_dish(
        self,
        dish_id: int,
        obj_in: DishUpdate,
        session: AsyncSession
    ) -> Dish:
        if obj_in.image:
            obj_in.image = await self.save_image(obj_in.image)
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
