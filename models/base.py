from types import SimpleNamespace

from sqlalchemy.orm import DeclarativeBase, selectinload, class_mapper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, column, insert
from typing import Sequence, Self
from fastapi import HTTPException, status


class Base(DeclarativeBase):
    async def save(self, db: AsyncSession, auto_commit: bool = True) -> Self:
        db.add(self)
        if auto_commit:
            await db.commit()
            await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession) -> None:
        await db.delete(self)

    async def update(
        self, db: AsyncSession, auto_commit: bool = True, **kwargs
    ) -> Self:
        for key, value in kwargs.items():
            setattr(self, key, value)

        if auto_commit:
            await db.commit()
            await db.refresh(self)
        return self

    @classmethod
    async def get_all(cls, db: AsyncSession, with_eager_loading: bool = False):

        options = []
        if with_eager_loading:
            for rel in class_mapper(cls).relationships:
                options.append(selectinload(getattr(cls, rel.key)))

        stmt = select(cls).options(*options)
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_first_model(cls, db: AsyncSession) -> Self | None:
        stmt = select(cls).limit(1)
        result = await db.scalars(stmt)
        return result.first()

    @classmethod
    async def find(
        cls, db: AsyncSession, raise_: bool = False, with_eager_loading: bool = False, **kwargs
    ) -> Self | None:

        options = []
        if with_eager_loading:
            for rel in class_mapper(cls).relationships:
                options.append(selectinload(getattr(cls, rel.key)))

        stmt = select(cls).filter_by(**kwargs).options(*options)
        result = await db.execute(stmt)
        result = result.scalars().first()
        if not result and raise_:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Instance of {cls.__name__} with specified parameters was not found",
            )
        return result

    @classmethod
    async def find_all(
        cls, db: AsyncSession, with_eager_loading: bool = False, **kwargs
    ) -> Sequence[Self]:
        query_criteria = []
        for key, value in kwargs.items():
            if isinstance(value, list):
                query_criteria.append(column(key).in_(value))
            else:
                query_criteria.append(column(key).__eq__(value))

        options = []
        if with_eager_loading:
            for rel in class_mapper(cls).relationships:
                options.append(selectinload(getattr(cls, rel.key)))

        stmt = select(cls).where(*query_criteria).options(*options)
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def create_all(cls, db: AsyncSession, data: list[dict]) -> None:
        stmt = insert(cls)
        await db.execute(stmt, data)

    # @classmethod
    # async def get_model_by_attribute(cls, db: AsyncSession, attribute: str, attribute_value: Any) -> Self | None:
    #     if hasattr(cls, attribute):
    #         model_attribute = getattr(cls, attribute)
    #         stmt = select(cls).where(model_attribute == attribute_value).limit(1)
    #         result = await db.scalars(stmt)
    #         return result.first()
    #     else:
    #         raise AttributeError(f"Attribute {attribute} Doesn't exist on {cls.__name__} Model")
    #
    # @classmethod
    # async def get_models_by_attribute(cls, db: AsyncSession, attribute: str, attribute_value: Any) -> list[Self] | Any:
    #     if hasattr(cls, attribute):
    #         model_attribute = getattr(cls, attribute)
    #         stmt = select(cls).where(model_attribute == attribute_value)
    #         result = await db.scalars(stmt)
    #         return result.all()
    #     else:
    #         raise AttributeError(f"Attribute {attribute} Doesn't exist on {cls.__name__} Model")
    #
    # @classmethod
    # async def create(cls, db: AsyncSession, *, obj_in: BaseModel | dict[str: Any]) -> Self:
    #     # obj_in_data = jsonable_encoder(obj_in)
    #
    #     # Check if obj_in is a dictionary or a Pydantic model
    #     if isinstance(obj_in, dict):
    #         db_obj = cls(**obj_in)
    #     else:
    #         db_obj = cls(**obj_in.model_dump(exclude_unset=True, exclude_none=True))
    #     db.add(db_obj)
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj
    #
    # @classmethod
    # async def update_model_by_attribute(cls, db: AsyncSession, *, attribute: str, attribute_value: Any,
    #                                     obj_in: BaseModel | dict[str: Any]):
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.model_dump(exclude_unset=True)
    #
    #     db_obj = await cls.get_model_by_attribute(db, attribute, attribute_value)
    #
    #     if not db_obj:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail=f"Couldn't find an object of {cls.__name__} with {attribute} = {attribute_value}")
    #
    #     for field in update_data:
    #         # getattr will get the current value of the field
    #         # only update fields different values than the current
    #         # comparison will work because everything will be of type string
    #         if getattr(db_obj, field) != update_data[field]:
    #             setattr(db_obj, field, update_data[field])
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj

    @classmethod
    async def remove_model_by_attribute(
        cls, db: AsyncSession, *, attribute: str, attribute_value: any
    ) -> None:
        if hasattr(cls, attribute):
            model_attribute = getattr(cls, attribute)
            stmt = select(cls).where(model_attribute == attribute_value)
            result = await db.scalars(stmt)
            obj = result.first()
            await db.delete(obj)
            await db.commit()
        else:
            raise AttributeError(
                f"Attribute {attribute} Doesn't exist on {cls.__name__} Model"
            )

    @classmethod
    async def remove_models_by_attribute(
        cls, db: AsyncSession, attribute: str, attribute_value: any
    ) -> SimpleNamespace:
        if hasattr(cls, attribute):
            model_attribute = getattr(cls, attribute)
            stmt = delete(cls).where(model_attribute == attribute_value)
            await db.execute(stmt)
            return SimpleNamespace(success=True)
        else:
            raise AttributeError(
                f"Attribute {attribute} Doesn't exist on {cls.__name__} Model"
            )
