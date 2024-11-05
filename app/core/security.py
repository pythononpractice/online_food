from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_user import user_crud
from app.models.user import User
from app.schemas.user import TokenData
from app.core.db import get_async_session

# Создаем объект для извлечения токена из заголовков Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_token(token: str) -> TokenData:
    """
    Проверяет и декодирует токен JWT. Если токен действителен, возвращает `TokenData`.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен недействителен или истек",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_email: int = payload.get("sub")

    if user_email is None:
        raise credentials_exception

    return TokenData(email=user_email)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    # Декодируем токен и извлекаем информацию о пользователе
    token_data = verify_token(token)
    user_email = token_data.email if token_data else None

    # Проверяем, существует ли пользователь в базе данных
    user = await user_crud.get_user_by_email(db=db, email=user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа",
        )
    return current_user