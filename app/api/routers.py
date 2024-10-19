from fastapi import APIRouter
from app.api.endpoints import auth_router

main_router = APIRouter()
main_router.include_router(auth_router, tags=['Authentication'], prefix='/auth')