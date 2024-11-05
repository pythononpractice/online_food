from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_admin
from app.models import User
from app.schemas.dish import DishCreate, DishUpdate, DishOut
from app.services import dish_service
from app.core.db import get_async_session

router = APIRouter()


@router.get("/restaurants/{restaurant_id}/menu/", response_model=List[DishOut])
async def get_menu(restaurant_id: int, db: AsyncSession = Depends(get_async_session)):
    return await dish_service.list_dishes(session=db, restaurant_id=restaurant_id)


@router.post("/restaurants/{restaurant_id}/menu/", response_model=DishOut)
async def create_dish(
    restaurant_id: int,
    dish: DishCreate,
    db: AsyncSession = Depends(get_async_session),
    current_admin: User = Depends(get_current_admin)
):
    return await dish_service.create_dish(session=db, restaurant_id=restaurant_id, obj_in=dish)


@router.put("/restaurants/{restaurant_id}/menu/{dish_id}/", response_model=DishOut)
async def update_dish(
    restaurant_id: int,
    dish_id: int,
    dish: DishUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_admin: User = Depends(get_current_admin)
):
    return await dish_service.update_dish(session=db, dish_id=dish_id, obj_in=dish)


@router.delete("/restaurants/{restaurant_id}/menu/{dish_id}/")
async def delete_dish(
    restaurant_id: int,
    dish_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_admin: User = Depends(get_current_admin)
):
    await dish_service.delete_dish(session=db, dish_id=dish_id)
