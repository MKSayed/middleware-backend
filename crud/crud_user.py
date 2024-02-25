from typing import Optional

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models.models_user import User
from schemas.schemas_user import UserCreate, UserBase, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # Declare model specific CRUD operation methods.
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_all_users(self, db: Session) -> list[User]:
        return db.query(User).all()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            password=get_password_hash(obj_in.password),
            name=obj_in.name,
            national_id=obj_in.national_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data.keys():
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def admin_update(self, db: Session, db_obj: User, obj_in: UserBase) -> User:
    #     update_data = obj_in.model_dump(exclude_unset=True)
    #     if update_data["password"]:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_user = CRUDUser(User)
