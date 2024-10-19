from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.crud.crud_user import user_crud
from app.models.user import User
from fastapi import HTTPException
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.schemas.user import CreateUserInDb

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def register_user(db: AsyncSession, email: str, password: str):
    # Проверяем, что пользователь не существует
    user_in_db = await user_crud.get_user_by_email(db=db, email=email)

    if user_in_db:
        raise HTTPException(status_code=400, detail="Такой пользователь уже есть!")

    # Создаем нового пользователя
    new_user = CreateUserInDb(
        email=email,
        hashed_password=hash_password(password)
    )
    await user_crud.create(obj_in=new_user, session=db)

    # Генерация access и refresh токенов
    access_token = create_access_token({"sub": new_user.email})
    refresh_token = create_refresh_token({"sub": new_user.email})

    return {"access_token": access_token, "refresh_token": refresh_token}


async def authenticate_user(db: AsyncSession, email: str, password: str):
    # Ищем пользователя по email
    user = await user_crud.get_user_by_email(db=db, email=email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Генерация access и refresh токенов
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token}


async def refresh_access_token(refresh_token: str):
    decoded_payload = decode_token(refresh_token)

    if not decoded_payload or "sub" not in decoded_payload:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    # Генерируем новый access токен
    new_access_token = create_access_token({"sub": decoded_payload["sub"]})
    return {"access_token": new_access_token}
