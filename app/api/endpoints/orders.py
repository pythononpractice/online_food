from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.models import User
from app.schemas.order import OrderCreate, OrderUpdate
from app.core.db import get_async_session
from app.services.order_service import order_service

router = APIRouter()


@router.post("/")
async def create_order(
        order: OrderCreate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    return await order_service.create_order(session=db, obj_in=order, user_id=current_user.id)


@router.get("/{order_id}/")
async def get_order(
        order_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    return await order_service.get_order(session=db, order_id=order_id)


@router.put("/{order_id}/status/")
async def update_order_status(
        order_id: int, status: OrderUpdate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    return await order_service.update_order_status(session=db, order_id=order_id, status=status.status)


@router.delete("/{order_id}/")
async def cancel_order(
        order_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    return await order_service.cancel_order(session=db, order_id=order_id)
