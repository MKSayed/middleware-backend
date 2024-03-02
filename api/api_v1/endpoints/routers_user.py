from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.exc import IntegrityError

from api.deps import SessionDep, CurrentUser
from schemas import UserBase, UserCreate, UserUpdate, UserDisplay, UserTypeBase
from crud.crud_user import crud_user, crud_user_type

router = APIRouter()


@router.get("", response_model=list[UserDisplay])
def get_all_users(db: SessionDep, current_user: CurrentUser):
    return crud_user.get_all(db)


@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: SessionDep,
                current_user: CurrentUser):
    try:
        return crud_user.create(db, obj_in=request)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


@router.put("/update/{id}", response_model=UserDisplay)
def update_user(id: int, db: SessionDep, user_update: UserUpdate,
                current_user: CurrentUser):
    print(user_update)
    try:
        user = crud_user.get_model_by_attribute(db, "id", id)
        return crud_user.update(db, db_obj=user, obj_in=user_update)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Failed to update user")
