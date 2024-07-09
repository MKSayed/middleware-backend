from fastapi import APIRouter, status, Query
from pydantic import TypeAdapter

from api.deps import AsyncSessionDep

from models.models_authority import (
    Application,
    Permission,
    Authority,
    AuthorizedRole,
    AssignedRole,
)
from schemas.schemas_authority import (
    ApplicationBase,
    AuthorizedRoleCreate,
    AuthorityCreate,
    AuthorityDisplay,
    PermissionDisplay,
    PermissionUpdate,
    PermissionCreate,
    AuthorityUpdate,
    AssignedRoleBase,
    AuthorityCreateOrUpdate,
    AssignedRoleCreateOrUpdate,
    PermissionDisplayShort,
    AuthorizedRoleBase,
)

router = APIRouter()


# current_user: CurrentUser


# Application related endpoints
@router.post("/new-application")
async def create_application(request: ApplicationBase, db: AsyncSessionDep):
    return await Application(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get("/all-applications", response_model=list[ApplicationBase])
async def get_all_applications(db: AsyncSessionDep):
    return await Application.get_all(db)


# Permission related endpoints
@router.get(
    "/all-permissions", response_model=list[PermissionDisplay | PermissionDisplayShort]
)
async def get_all_permissions(
    db: AsyncSessionDep,
    short: bool | None = Query(
        False, description="Whether to return the short version of the data"
    ),
):
    permissions = await Permission.get_all(db)
    if short:
        short_permissions_adapter = TypeAdapter(list[PermissionDisplayShort])
        return short_permissions_adapter.validate_python(permissions)
    return permissions


@router.post("/new-permission")
async def create_permission(request: PermissionCreate, db: AsyncSessionDep):
    return await Permission(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.put("/update-permission/{pk}")
async def update_permission(pk, request: PermissionUpdate, db: AsyncSessionDep):
    permission = await Permission.find(db, number=pk)
    return await permission.update(
        db, **request.model_dump(exclude_unset=True, exclude_none=True)
    )


# Roles related endpoints
@router.get(
    "/all-roles", response_model=list[AuthorizedRoleBase | AuthorizedRoleCreate]
)
async def get_all_roles(
    db: AsyncSessionDep,
    short: bool | None = Query(
        False, description="Whether to return the short version of the data"
    ),
):
    authorized_roles = await AuthorizedRole.get_all(db)
    if short:
        short_authorized_roles_adapter = TypeAdapter(list[AuthorizedRoleCreate])
        return short_authorized_roles_adapter.validate_python(authorized_roles)
    return authorized_roles


@router.get("/all-role-data-for-role/{role_number}")
async def get_role_permissions(db: AsyncSessionDep, role_number: int):
    authorized_role = await AuthorizedRole.find(db, number=role_number)
    active_authorities = await Authority.find_all(
        db, fk_authorized_rnumber=role_number, active=1
    )
    role_permissions = []
    for authority in active_authorities:
        role_permissions.append(authority.permission)

    role_permissions_short = [
        {"number": permission.number, "name": permission.name}
        for permission in role_permissions
    ]

    return {
        "roleData": {
            "name": authorized_role.name,
            "number": authorized_role.number,
            "permissions": role_permissions_short,
        }
    }


@router.post("/new-role")
async def create_role(request: AuthorizedRoleCreate, db: AsyncSessionDep):
    return await AuthorizedRole(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.put("/update-role/{pk}")
async def update_role(pk, request: AuthorizedRoleCreate, db: AsyncSessionDep):
    authorized_role = await AuthorizedRole.find(db, number=pk)
    return await authorized_role.update(
        db, **request.model_dump(exclude_unset=True, exclude_none=True)
    )


# Authority related endpoints
@router.get("/all-authorities", response_model=list[AuthorityDisplay])
async def get_all_authorities(db: AsyncSessionDep):
    return await Authority.get_all(db)


@router.post("/new-authority")
async def create_authority(request: AuthorityCreate, db: AsyncSessionDep):
    return await Authority(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.put("/update-authority/{pk}")
async def update_authority(pk, request: AuthorityUpdate, db: AsyncSessionDep):
    authority = await Authority.find(db, serial=pk)
    return await authority.update(
        db, **request.model_dump(exclude_unset=True, exclude_none=True)
    )


@router.post("/manage-role-authorities", status_code=status.HTTP_200_OK)
async def manage_role_authority(request: AuthorityCreateOrUpdate, db: AsyncSessionDep):
    authorized_rnumber = request.authorized_rnumber
    new_permission_numbers = request.permission_numbers
    current_permission_numbers = []
    old_authorities = await Authority.find_all(
        db, fk_authorized_rnumber=authorized_rnumber
    )

    # Deactivate/reactivate existing authorities for this role
    for old_authority in old_authorities:
        current_permission_numbers.append(old_authority.fk_permission_number)
        if old_authority.fk_permission_number not in new_permission_numbers:
            await old_authority.update(db, auto_commit=False, active="0")
        elif str(old_authority.active) == "0":
            await old_authority.update(db, auto_commit=False, active="1")

    # Create newly set authorities for this role
    for permission_number in new_permission_numbers:
        if permission_number not in current_permission_numbers:
            await Authority(
                fk_authorized_rnumber=authorized_rnumber,
                fk_permission_number=permission_number,
                active=1,
            ).save(db, auto_commit=False)

    # Update role name
    authorized_role = await AuthorizedRole.find(db, number=authorized_rnumber)
    await authorized_role.update(db, name=request.authorized_rname)

    # Commit all changes in this session
    await db.commit()

    return {"message": "success"}


# AssignedRole related endpoints
@router.post("/manage-user-roles", status_code=status.HTTP_200_OK)
async def manage_user_roles(request: AssignedRoleCreateOrUpdate, db: AsyncSessionDep):
    user_id = request.user_id
    new_role_numbers = request.role_numbers
    current_assigned_roles_numbers = []
    current_assigned_roles = await AssignedRole.find_all(db, fk_userid=user_id)

    # Deactivate/reactivate existing roles for this user
    for current_assigned_role in current_assigned_roles:
        current_assigned_roles_numbers.append(
            current_assigned_role.fk_authorized_rnumber
        )
        if current_assigned_role.fk_authorized_rnumber not in new_role_numbers:
            await current_assigned_role.update(db, auto_commit=False, active="0")
        elif str(current_assigned_role.active) == "0":
            await current_assigned_role.update(db, auto_commit=False, active="1")

    # Create newly set authorities for this role
    for role_number in new_role_numbers:
        if role_number not in current_assigned_roles_numbers:
            await AssignedRole(
                fk_userid=user_id, fk_authorized_rnumber=role_number, active=1
            ).save(db, auto_commit=False)

    # Commit all changes in this session
    await db.commit()

    return {"message": "success"}


@router.get(
    "/current-assigned-roles/{fk_userid}", response_model=list[AssignedRoleBase]
)
async def get_current_assigned_roles(fk_userid: int, db: AsyncSessionDep):
    return await AssignedRole.find_all(db, fk_userid=fk_userid, active="1")
