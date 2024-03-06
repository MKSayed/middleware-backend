from sqlalchemy.orm import Session

from core.security import get_password_hash
from crud.base import CRUDBase
from models.models_user import User, UserType
from schemas.schemas_user import UserCreate, UserUpdate


class CRUDUser(CRUDBase):
    # Declare model specific CRUD operation methods.

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            password=get_password_hash(obj_in.password),
            name=obj_in.name,
            national_id=obj_in.national_id,
            status=obj_in.status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)

        # Do not update password if sent as empty string
        if password := update_data.get("password"):
            hashed_password = get_password_hash(password)
            del update_data["password"]
            update_data["password"] = hashed_password
        else:
            # Make sure no empty string is being sent to database
            del update_data["password"]

        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_user = CRUDUser(User)


class CRUDUserType(CRUDBase):
    pass


crud_user_type = CRUDUserType(UserType)
