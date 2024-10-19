from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        db_obj = db_obj.scalar()
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            # user: Optional[User] = User(id=1)
    ):
        try:
            obj_in_data = obj_in.dict()
            # if user is not None:
            #     obj_in_data['id_user'] = user.id
            db_obj = self.model(**obj_in_data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            raise HTTPException(status_code=422, detail=f"Такой объект уже существует.")

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_ids(
            self,
            obj_ids: list[int],
            session: AsyncSession, ):
        modules = await session.execute(
            select(self.model).where(self.model.id.in_(obj_ids)))
        return modules.scalars().all()
