from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.deps import SessionDep, get_current_user
from schemas import schemas_user
from crud.crud_user import crud_user

router = APIRouter()


@router.get("", response_model=list[schemas_user.UserDisplay])
def get_all_users(db: SessionDep, current_user: Annotated[schemas_user.UserBase, Depends(get_current_user)]):
    return crud_user.get_all_users(db)


@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas_user.UserCreate, db: SessionDep,
                current_user: Annotated[schemas_user.UserBase, Depends(get_current_user)]):
    try:
        return crud_user.create(db, obj_in=request)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


@router.put("/update/{id}", response_model=schemas_user.UserDisplay)
def update_user(id: int, db: SessionDep, updated_user: schemas_user.UserUpdate,
                current_user: Annotated[schemas_user.UserBase, Depends(get_current_user)]):
    user = crud_user.get(db, id)
    try:
        return crud_user.update(db, user, updated_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")



# @router.get('/', response_model=list[UserBase])
# def get_all_users(db: Session = Depends(get_db)):
#     return user_controller.get_all_users(db)
#
#
# @router.get('/{id}', response_model=UserBase)
# def get_user(id: int, db: Session = Depends(get_db)):
#     return user_controller.get_user(db, id)