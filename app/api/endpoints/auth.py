from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import CreateAdminUser, LoginUser
from app.services import auth_service
from app.core.db import get_async_session

router = APIRouter()

# Регистрация нового пользователя
@router.post("/register/")
async def register(user: CreateAdminUser, db: AsyncSession = Depends(get_async_session)):
    tokens = await auth_service.register_user(db, user.email, user.password)
    return tokens


# Вход пользователя
@router.post("/login/")
async def login(user: LoginUser, db: AsyncSession = Depends(get_async_session)):
    tokens = await auth_service.authenticate_user(db, user.email, user.password)
    return tokens


# Обновление access токена через refresh токен
@router.post("/refresh/")
async def refresh(refresh_token: str):
    tokens = await auth_service.refresh_access_token(refresh_token)
    return tokens
