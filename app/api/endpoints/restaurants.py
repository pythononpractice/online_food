from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.security import get_current_admin
from app.models import User
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantBase
from app.services import restaurant_service


router = APIRouter()


# Получение списка ресторанов
@router.get("/", response_model=List[RestaurantBase])
async def get_restaurants(db: AsyncSession = Depends(get_async_session)):
    return await restaurant_service.list_restaurants(db)


# Получение информации о конкретном ресторане
@router.get("/{restaurant_id}", response_model=RestaurantBase)
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_async_session)):
    restaurant = await restaurant_service.get_restaurant(session=db, restaurant_id=restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


# Добавление нового ресторана (только для администратора)
@router.post("/", response_model=RestaurantBase)
async def create_restaurant(
    restaurant: RestaurantCreate,
    db: AsyncSession = Depends(get_async_session),
    current_admin: User = Depends(get_current_admin)
):
    return await restaurant_service.create_restaurant(session=db, obj_in=restaurant)


# Обновление ресторана (только для администратора)
@router.put("/{restaurant_id}", response_model=RestaurantBase)
async def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_admin: User = Depends(get_current_admin)
):
    return await restaurant_service.update_restaurant(session=db, restaurant_id=restaurant_id, obj_in=restaurant_data)


# Удаление ресторана (только для администратора)
@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_admin: User = Depends(get_current_admin)
):
    await restaurant_service.delete_restaurant(session=db, restaurant_id=restaurant_id)