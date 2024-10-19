import datetime
from fastapi import HTTPException

from pydantic import BaseModel, EmailStr, validator, constr


from typing import Optional, List

from pydantic import BaseModel

from app.crud.crud_user import user_crud


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class BaseUser(BaseModel):
    id: int
    email: EmailStr
    # name: str

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    id: Optional[int]
    email: Optional[str] = None
    # name: Optional[str] = None
    password: Optional[str] = None


class UpdateUserForOrg(BaseModel):
    email: Optional[EmailStr] = None
    # name: Optional[constr(min_length=1, max_length=50, regex=r'^[А-Яа-яЁё]+$')] = None
    password: Optional[str] = None

    @validator("password")
    def validate_password(cls, value):
        # Ваша валидация пароля здесь
        if not validate_password(value):
            raise ValueError("Невалидный пароль. Убедитесь, что новый пароль соответствует требованиям.")
        return value


class UpdateUserInDb(BaseModel):
    id: int
    email: Optional[str] = None
    # name: Optional[str] = None
    hashed_password: Optional[str] = None


class CreateAdminUser(BaseModel):
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str



class CreateUserInDb(BaseModel):
    email: EmailStr

    hashed_password: str






class UpdatePassword(BaseModel):
    old_password: str
    new_password: str

    @validator("new_password")
    def validate_new_password(cls, value):
        # Ваша валидация пароля здесь
        if not validate_password(value):
            raise ValueError("Невалидный пароль. Убедитесь, что новый пароль соответствует требованиям.")
        return value


class PasswordGenerate(BaseModel):
    password: str


class UpdatePasswordAdmin(BaseModel):
    new_password: str

    @validator("new_password")
    def validate_new_password(cls, value):
        # Ваша валидация пароля здесь
        if not validate_password(value):
            raise ValueError("Невалидный пароль. Убедитесь, что новый пароль соответствует требованиям.")
        return value
