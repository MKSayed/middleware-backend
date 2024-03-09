from sqlalchemy import Select, insert
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_authority import Application, Permission, Authority, AuthorizedRole, AssignedRole
from schemas.schemas_authority import AuthorityCreate


class CRUDApplication(CRUDBase):
    pass


crud_application = CRUDApplication(Application)


class CRUDPermission(CRUDBase):
    @staticmethod
    def get_all_name_number(db: Session):
        stmt = Select(Permission.number, Permission.name)
        return db.execute(stmt).mappings().all()



crud_permission = CRUDPermission(Permission)


class CRUDAuthority(CRUDBase):
    def create(self, db: Session, *, obj_in: AuthorityCreate):
        stmt = insert(Authority).values(**obj_in.model_dump(exclude_unset=True, exclude_none=True))
        db_obj = db.execute(stmt)
        db.commit()
        db.refresh(db_obj)
        return obj_in


crud_authority = CRUDAuthority(Authority)


class CRUDAuthorizedRole(CRUDBase):
    pass


crud_authorized_role = CRUDAuthorizedRole(AuthorizedRole)


class CRUDAssignedRole(CRUDBase):
    @staticmethod
    def check_role_exists(db: Session, fk_authorized_rnumber: int, fk_userid: int):
        stmt = Select(AssignedRole).where(AssignedRole.fk_authorized_rnumber == fk_authorized_rnumber,
                                          AssignedRole.fk_userid == fk_userid)
        return db.scalar(stmt)

    @staticmethod
    def get_current_roles(db: Session, fk_userid: int):
        stmt = Select(AssignedRole).where(AssignedRole.fk_userid == fk_userid)
        return db.scalars(stmt)


crud_assigned_role = CRUDAssignedRole(AssignedRole)
