from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.exc import IntegrityError

from api.deps import SessionDep, CurrentUser
from schemas.schemas_user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserDisplay,
    UserTypeBase,
)
from crud.crud_user import crud_user, crud_user_type

router = APIRouter()


@router.get("/users", response_model=list[UserDisplay])
async def get_all_users(db: SessionDep, current_user: CurrentUser):
    return crud_user.get_all(db)


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate, db: SessionDep):

    try:
        return crud_user.create(db, obj_in=request)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )


@router.put("/users/{pk}", response_model=UserDisplay)
async def update_user(pk: int, db: SessionDep, user_update: UserUpdate):
    try:
        user = crud_user.get_model_by_attribute(db, "id", pk)
        return crud_user.update(db, db_obj=user, obj_in=user_update)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Failed to update user"
        )
