from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_base import CRUDBase
from app.models import User


class CRUDUser(CRUDBase):
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str):
        user = await db.execute(select(User).filter(User.email == email).limit(1))
        return user.scalar()

    # async def save_avatar(self, avatar: str):
    #     """return avatar image path"""
    #     # try:
    #     img_type = avatar.split('/')[1].split(';')[0]
    #     image = base64.b64decode(avatar.split(',')[-1])
    #     name = uuid.uuid4()
    #     filename = os.getcwd() + f"{settings.media_path}/users/{name}.{img_type}"
    #     with open(filename, 'wb') as f:
    #         f.write(image)
    #
    #     # result = b64tf.save(avatar, f'{settings.media_path}/users/')
    #
    #     return settings.backend_url + f"{settings.media_path}/users/{name}.{img_type}"

    async def update_password(self, user_id: int, new_password: str, session: AsyncSession):
        # Получаем пользователя из базы данных
        user = await session.get(User, user_id)

        if not user:
            return None  # Можно также выбросить исключение HTTPException с кодом 404

        # Обновляем поле с хешированным паролем
        user.hashed_password = new_password

        # Сохраняем изменения в базе данных
        await session.commit()

        return user





user_crud = CRUDUser(User)
