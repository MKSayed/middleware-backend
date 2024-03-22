from fastapi import APIRouter, HTTPException, status
from typing import List
from models import models_kiosk, models_sevice, models_commission, models_address, models_connector, models_equipment

from api.deps import SessionDep, CurrentUser
from crud.crud_authority import (crud_application, crud_permission, crud_authorized_role,
                                 crud_authority, crud_assigned_role)

from schemas.schemas_authority import (ApplicationBase, AuthorizedRoleCreate, AuthorityCreate, AuthorityDisplay,
                                       PermissionDisplay, PermissionUpdate, PermissionCreate, AuthorityUpdate,
                                       AssignedRoleBase, AuthoritiesCreateOrUpdate)

router = APIRouter()


# current_user: CurrentUser


# Application related endpoints
@router.post("/new-application")
def create_application(request: ApplicationBase, db: SessionDep):
    return crud_application.create(db, obj_in=request)


@router.get("/all-applications", response_model=List[ApplicationBase])
async def get_all_applications(db: SessionDep):
    return crud_application.get_all(db)


# Permission related endpoints
@router.get("/all-permissions", response_model=List[PermissionDisplay])
async def get_all_permissions(db: SessionDep):
    return crud_permission.get_all(db)


@router.get("/all-permissions-short", response_model=List[AuthorityDisplay.AuthorityPermissionDisplay])
async def get_all_permissions_short(db: SessionDep):
    return crud_permission.get_all(db)


@router.post("/new-permission")
async def create_permission(request: PermissionCreate, db: SessionDep):
    return crud_permission.create(db, obj_in=request)


@router.put("/update-permission/{pk}")
async def create_permission(pk, request: PermissionUpdate, db: SessionDep):
    db_obj = crud_permission.get_model_by_attribute(db, "number", pk)
    return crud_permission.update(db, db_obj=db_obj, obj_in=request)


# Roles related endpoints
@router.get("/all-roles")
def get_all_roles(db: SessionDep):
    return crud_authorized_role.get_all(db)


@router.get("/all-roles-short", response_model=List[AuthorityDisplay.AuthorityAuthorizedRoleDisplay])
async def get_all_roles_short(db: SessionDep):
    return crud_authorized_role.get_all(db)


@router.get("/get-role-permissions/{role_number}")
async def get_role_short(db: SessionDep, role_number: int):
    role_data = crud_authorized_role.get_model_by_attribute(db, "number", role_number)
    role_permissions = crud_authorized_role.get_active_role_permissions(db, role_number)

    role_permissions_short = [{"number": permission.number, "name": permission.name}
                              for permission in role_permissions]

    return {"roleData": {"name": role_data.name, "number": role_data.number, "permissions": role_permissions_short}}

@router.post("/new-role")
def create_role(request: AuthorizedRoleCreate, db: SessionDep):
    return crud_authorized_role.create(db, obj_in=request)


@router.put("/update-role/{pk}")
def create_role(pk, request: AuthorizedRoleCreate, db: SessionDep):
    db_obj = crud_authorized_role.get_model_by_attribute(db, "number", pk)
    return crud_authorized_role.update(db, db_obj=db_obj, obj_in=request)


# Authority related endpoints
@router.get("/all-authorities", response_model=List[AuthorityDisplay])
def get_all_authorities(db: SessionDep):
    return crud_authority.get_all(db)


@router.post("/new-authority")
def create_authority(request: AuthorityCreate, db: SessionDep):
    return crud_authority.create(db, obj_in=request)


@router.put("/update-authority/{pk}")
def create_role(pk, request: AuthorityUpdate, db: SessionDep):
    db_obj = crud_authority.get_model_by_attribute(db, "serial", pk)
    return crud_authorized_role.update(db, db_obj=db_obj, obj_in=request)


@router.post("/manage-role-authorities", status_code=status.HTTP_200_OK)
def manage_authority(request: AuthoritiesCreateOrUpdate, db: SessionDep):
    authorized_rnumber = request.authorized_rnumber
    permission_numbers = request.permission_numbers
    current_permission_numbers = []
    current_authorities = crud_authority.get_models_by_attribute(db, "fk_authorized_rnumber", authorized_rnumber)

    # Deactivate/reactivate existing authorities for this role
    for current_authority in current_authorities:
        current_permission_numbers.append(current_authority.fk_permission_number)
        if current_authority.fk_permission_number not in permission_numbers:
            current_authority.active = '0'
        elif str(current_authority.active) == '0':
            current_authority.active = '1'

    # Create newly set authorities for this role
    for permission_number in permission_numbers:
        if permission_number not in current_permission_numbers:
            crud_authority.create(db, obj_in={"fk_authorized_rnumber": authorized_rnumber,
                                              "fk_permission_number": permission_number,
                                              "active": 1})

    # Update role name
    authorized_role = crud_authorized_role.get_model_by_attribute(db, "number", authorized_rnumber)
    authorized_role.name = request.authorized_rname

    # Commit all changes in this session
    db.commit()


# AssignedRole related endpoints
@router.post("/new-assigned-roles")
def create_assigned_role(request: List[AssignedRoleBase], db: SessionDep):
    updated_roles = 0
    for assigned_role in request:
        if crud_assigned_role.check_role_exists(db=db, fk_authorized_rnumber=assigned_role.fk_authorized_rnumber,
                                                fk_userid=assigned_role.fk_userid):
            continue
        else:
            updated_roles += 1
            crud_assigned_role.create(db=db, obj_in=assigned_role)
    if updated_roles == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No changes.")
    return {"message": "Role(s) has been added successfully"}


@router.get("/current-assigned-roles/{fk_userid}", response_model=List[AssignedRoleBase])
def get_current_assigned_roles(fk_userid: int, db: SessionDep):
    return crud_assigned_role.get_current_roles(db, fk_userid=fk_userid)

