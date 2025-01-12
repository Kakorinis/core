from sqlalchemy import select, delete

from typing import Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from core.schemas.dtos import BaseSchema
from core.models import MixinAutoIdModel


ModelType = TypeVar('ModelType', bound=MixinAutoIdModel)
DtoType = TypeVar('DtoType', bound=BaseSchema)


class BaseRepository:
    def __init__(
            self,
            session_maker: sessionmaker,
            model: Type[ModelType],
            with_id_dto: Type[DtoType]
    ):
        self.session_maker = session_maker
        self.table_model = model
        self.with_id_dto = with_id_dto

    async def get_one_by_id(self, id_: int) -> BaseSchema | None:
        async with self.session_maker as session:
            stmt = select(self.table_model).where(self.table_model.id == id_)
            model = await session.scalar(stmt)
            if not model:
                return None
            return self.with_id_dto.model_validate(model)

    async def add_one(self, data_schema: BaseSchema) -> BaseSchema:
        async with self.session_maker() as session:
            new_user = self.table_model(**data_schema.dict())
            session.add(new_user)
            # await session.flush()
            await session.commit()
            return self.with_id_dto.model_validate(new_user)

    async def update_one(self, data_schema: BaseModel):
        async with self.session_maker() as session:
            user = self.table_model(**data_schema.dict())
            updated_user = await session.merge(user)
            # session.flush()
            await session.commit()
            return self.with_id_dto.model_validate(updated_user)

    async def delete_one_by_id(self, object_id: int) -> bool:
        async with self.session_maker() as session:
            statement = delete(
                self.table_model
            ).where(
                self.table_model.id == object_id
            )
            await session.execute(statement)
            await session.commit()
            return True
