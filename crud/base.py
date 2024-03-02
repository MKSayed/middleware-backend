from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from types import SimpleNamespace

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Select, delete

from database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# Types are used here just for readability and doesn't enforce any type of validation
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get_model_by_attribute(self, db: Session, attribute: str, attribute_value: Any) -> Optional[ModelType]:
        if hasattr(self.model, attribute):
            model_attribute = getattr(self.model, attribute)
            stmt = Select(self.model).where(model_attribute == attribute_value).limit(1)
            return db.scalars(stmt).first()
        else:
            raise AttributeError

    def get_models_by_attribute(self, db: Session, attribute: str, attribute_value: Any) -> Optional[ModelType]:
        if hasattr(self.model, attribute):
            model_attribute = getattr(self.model, attribute)
            stmt = Select(self.model).where(model_attribute == attribute_value)
            return db.scalars(stmt).all()
        else:
            raise AttributeError

    def get_all(self, db: Session):
        stmt = Select(self.model)
        return db.scalars(stmt).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            # getattr will get the current value of the field
            # only update fields different values than the current
            # comparison will work because everything will be of type string
            if getattr(db_obj, field) != update_data[field]:
                setattr(db_obj, field, update_data[field])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_model_by_attribute(self, db: Session, *, attribute: str, attribute_value: any) -> ModelType:
        if hasattr(self.model, attribute):
            model_attribute = getattr(self.model, attribute)
            stmt = Select(self.model).where(model_attribute == attribute_value)
            obj = db.scalars(stmt).first()
            db.delete(obj)
            db.commit()
            return obj
        else:
            raise AttributeError

    def remove_models_by_attribute(self, db: Session, attribute: str, attribute_value: any) -> SimpleNamespace:
        if hasattr(self.model, attribute):
            model_attribute = getattr(self.model, attribute)
            stmt = delete(self.model).where(model_attribute == attribute_value)
            db.execute(stmt)
            return SimpleNamespace(success=True)
        else:
            raise AttributeError
