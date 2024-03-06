from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.deps import SessionDep, CurrentUser
from crud.crud_authority import crud_application, crud_permission, crud_authorized_role
from schemas.schemas_authority import ApplicationBase, PermissionCreate, AuthorizedRoleCreate

router = APIRouter()
# current_user: CurrentUser


# Application related endpoints
@router.post("/new-application")
def create_application(request: ApplicationBase, db: SessionDep):
    return crud_application.create(db, obj_in=request)


@router.get("/all-applications")
async def get_all_applications(db: SessionDep):
    return crud_application.get_all(db)


# Permission related endpoints
@router.get("/all-permissions")
async def get_all_permissions(db: SessionDep):
    return crud_permission.get_all(db)


@router.post("/new-permission")
async def create_permission(request: PermissionCreate, db: SessionDep):
    return crud_permission.create(db, obj_in=request)


@router.put("/update-permission/{pk}")
async def create_permission(pk, request: PermissionCreate, db: SessionDep):
    db_obj = crud_permission.get_model_by_attribute(db, "number", pk)
    return crud_permission.update(db, db_obj=db_obj, obj_in=request)


# Roles related endpoints
@router.get("/all-roles")
def get_all_roles(db: SessionDep):
    return crud_authorized_role.get_all(db)


@router.post("/new-role")
def create_role(request: AuthorizedRoleCreate, db: SessionDep):
    return crud_authorized_role.create(db, obj_in=request)


@router.put("/update-role/{pk}")
def create_role(pk, request: AuthorizedRoleCreate, db: SessionDep):
    db_obj = crud_authorized_role.get_model_by_attribute(db, "number", pk)
    return crud_authorized_role.update(db, db_obj=db_obj, obj_in=request)
