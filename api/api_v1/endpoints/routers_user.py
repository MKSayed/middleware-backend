from fastapi import APIRouter, Depends
from typing import Annotated

from api.deps import SessionDep, get_current_user
from schemas import schemas_user
from crud.crud_user import crud_user

router = APIRouter()


@router.post("/new")
def create_user(request: schemas_user.UserCreate, db: SessionDep):
    return crud_user.create(db, obj_in=request)


@router.get("/geto")
def get_user_by_username2(db: SessionDep,
                          current_user: Annotated[schemas_user.UserBase, Depends(get_current_user)]):
    return current_user


# @router.get('/', response_model=list[UserBase])
# def get_all_users(db: Session = Depends(get_db)):
#     return user_controller.get_all_users(db)
#
#
# @router.get('/{id}', response_model=UserBase)
# def get_user(id: int, db: Session = Depends(get_db)):
#     return user_controller.get_user(db, id)